from app.extensions import db
from app.models.comment import Comment


class CommentService:
    def getCommentsByEvent(self, event_id: int) -> list[Comment]:
        return (
            Comment.query
            .filter_by(event_id=event_id)
            .order_by(Comment.created_at.desc())
            .all()
        )

    def addComment(self, user_id: int, event_id: int, content: str) -> Comment:
        comment = Comment(user_id=user_id, event_id=event_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return comment
