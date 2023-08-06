"""General definitions for reviewers."""
import typing

import typing_extensions


class Comment(typing.NamedTuple):
    """A single review comment."""

    path: str
    line: int
    message: str
    col: typing.Optional[int] = None


class Reviewer(typing_extensions.Protocol):
    """Protocol for reviewers."""

    def post_comment(self, comment: Comment):
        """Post the given comment in the review."""

    def get_existing_comments(self) -> typing.List[Comment]:
        """Return the comments that already exist in the review."""

    def resolve_comment(self, comment: Comment):
        """Mark the given comment as resolved."""

    def get_changed_lines(self) -> typing.Mapping[str, typing.Iterable[int]]:
        """Get the lines changed in this review.

        Returns mapping of file_name: {lines_changed}
        """


class DryReviewer(Reviewer):
    """Reviewer that posts no comments."""

    def post_comment(self, comment: Comment):
        """Post no comments."""
        pass

    def get_existing_comments(self) -> typing.List[Comment]:
        """Return no comments."""
        return []

    def resolve_comment(self, comment: Comment):
        """Resolve no comments."""
        pass
