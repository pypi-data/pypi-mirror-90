"""Tools for posting gitlab reviews."""
import argparse
import os
import typing

import gitlab as gitlab_api

from . import diff
from .reviewer import Comment


class MergeRequestInfo(typing.NamedTuple):
    """Information needed to identify a merge request."""

    project_id: int
    mr_internal_id: int


def add_gitlab_args(parser: argparse.ArgumentParser):
    """Adds command line arguments associated with gitlab."""
    gitlab_args = parser.add_argument_group("gitlab")
    gitlab_args.add_argument(
        "--token", help="API token for gitlab, Is required for gitlab usage."
    )
    gitlab_args.add_argument(
        "--project",
        default=os.environ.get("CI_PROJECT_ID"),
        help="Project ID of the merge request, defaults to variable set by pipeline.",
    )
    gitlab_args.add_argument(
        "--merge_request",
        default=os.environ.get("CI_MERGE_REQUEST_IID"),
        help="Internal ID of the merge request, defaults to variable set by pipeline.",
    )


class GitlabReviewer:
    """Reviewer posting comments to gitlab."""

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "GitlabReviewer":
        """Creates an instance from user arguments."""
        if not args.token:
            raise ValueError("--token must be passed to use gitlab reviewer!")
        return cls(args.token, MergeRequestInfo(args.project, args.merge_request))

    def __init__(
        self,
        token: str,
        merge_request: MergeRequestInfo,
        gitlab_url: str = "https://gitlab.com",
    ) -> None:
        """Creates a gitlab reviewer reviewing a specific merge request."""
        self.gitlab = gitlab_api.Gitlab(gitlab_url, private_token=token)
        self.mr = self.gitlab.projects.get(merge_request.project_id).mergerequests.get(
            merge_request.mr_internal_id
        )
        self.discussions = self.mr.discussions.list()

    @property
    def _user(self):
        self.gitlab.auth()
        return self.gitlab.user

    def post_comment(self, comment: Comment):
        """Post a single comment as a new discussion.

        Batch reviews are not supported by gitlab api :(
        """
        try:
            self.mr.discussions.create(
                {
                    "body": comment.message,
                    "position": {
                        "new_path": comment.path,
                        "position_type": "text",
                        "new_line": int(comment.line),
                        **self.mr.diff_refs,
                    },
                },
            )
        except gitlab_api.GitlabCreateError as request_error:
            if "500 Internal Server Error" not in str(
                request_error
            ):  # Ignore 500 responses
                raise

    def _is_by_reviewer(self, note: dict) -> bool:
        return note["type"] == "DiffNote" and note["author"]["id"] == self._user.id

    def get_existing_comments(self) -> typing.List[Comment]:
        """Returns all comments posted by this reviewer on the merge request."""
        heading_notes = [
            self._heading_note(discussion) for discussion in self.discussions
        ]
        return [
            self._to_comment(note)
            for note in heading_notes
            if self._is_by_reviewer(note) and not note["resolved"]
        ]

    def get_changed_lines(self) -> typing.Mapping[str, typing.Iterable[int]]:
        """Get the lines changed in this review.

        Returns mapping of file_name: {lines_changed*}
        """
        changed_lines: typing.Dict[str, typing.Set[int]] = dict()
        for change in self.mr.changes()["changes"]:
            changed_lines.setdefault(change["new_path"], set()).update(
                diff.changed_lines_in_multiple_hunks(change["diff"].splitlines())
            )

        return changed_lines

    def resolve_comment(self, comment: Comment):
        """Resolve the relevant gitlab discussion where comment was posted."""
        discussion = {
            self._to_comment(self._heading_note(discussion)): discussion
            for discussion in self.discussions
            if self._is_by_reviewer(self._heading_note(discussion))
        }[comment]
        discussion.resolved = True
        discussion.save()

    @staticmethod
    def _heading_note(discussion):
        return discussion.attributes["notes"][0]

    @staticmethod
    def _to_comment(note: dict) -> Comment:
        position: dict = note["position"]
        return Comment(
            path=position["new_path"],
            message=note["body"],
            line=int(position["new_line"]),
            col=position.get("new_col"),
        )
