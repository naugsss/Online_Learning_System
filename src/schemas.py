from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class CourseSchema(Schema):
    name = fields.Str(required=True)
    duration = fields.Int(required=True)
    content = fields.Str(required=True)
    price = fields.Int(required=True)


class PurchaseCourseSchema(Schema):
    name = fields.Str(required=True)


class FeedbackSchema(Schema):
    ratings = fields.Float(required=True)
    comments = fields.Str()


class FaqSchema(Schema):
    questions = fields.Str(required=True)
    answers = fields.Str(required=True)


class MentorSchema(Schema):
    username = fields.Str(required=True)

class EarningSchema(Schema):
    name = fields.Str(required=True)
    course_name = fields.Str()
    earning = fields.Integer(required=True)