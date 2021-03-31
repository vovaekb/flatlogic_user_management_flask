from datetime import datetime, timezone
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import fields
from app import app
from app.models import Files, Users



class FilesSchema(SQLAlchemyAutoSchema):
    createdAt = fields.fields.Function(lambda obj: obj.createdAt.astimezone(timezone.utc).isoformat('T', timespec='milliseconds').replace('+00:00', 'Z'))
    updatedAt = fields.fields.Function(lambda obj: obj.updatedAt.astimezone(timezone.utc).isoformat('T', timespec='milliseconds').replace('+00:00', 'Z'))
    deletedAt = fields.fields.Function(lambda obj: obj.deletedAt.astimezone(timezone.utc).isoformat('T', timespec='milliseconds').replace('+00:00', 'Z') if not obj.deletedAt is None else None)
    class Meta:
        model = Files
        include_fk = True
        # include_relationships = True
        exclude = ("createdBy", "updatedBy", "userId") # "user", 
        # include_fk = True


class UsersSchema(SQLAlchemyAutoSchema):
    createdAt = fields.fields.Function(lambda obj: obj.createdAt.astimezone(timezone.utc).isoformat('T', timespec='milliseconds').replace('+00:00', 'Z'))
    updatedAt = fields.fields.Function(lambda obj: obj.updatedAt.astimezone(timezone.utc).isoformat('T', timespec='milliseconds').replace('+00:00', 'Z'))
    deletedAt = fields.fields.Function(lambda obj: obj.deletedAt.astimezone(timezone.utc).isoformat('T', timespec='milliseconds').replace('+00:00', 'Z') if not obj.deletedAt is None else None)
    class Meta:
        model = Users
        include_fk = True
        exclude = ("createdBy", "updatedBy")
        #include_relationships = True
