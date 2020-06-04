# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    bio = fields.Str()
    image = fields.Url()
    token = fields.Str()
    createdAt = fields.DateTime(attribute='created_at', dump_only=True)
    updatedAt = fields.DateTime(attribute='updated_at')
    occupation = fields.Str()
    githubLink = fields.Url()
    twitterLink = fields.Url()
    linkedinLink = fields.Url()
    website = fields.Url()
    # ugly hack.
    user = fields.Nested('self', exclude=('user',), default=True, load_only=True)

    @pre_load
    def make_user(self, data, **kwargs):
        data = data['user']
        # some of the frontends send this like an empty string and some send
        # null
        if not data.get('email', True):
            del data['email']
        if not data.get('image', True):
            del data['image']
        return data

    @post_dump
    def dump_user(self, data, **kwargs):
        return {'user': data}

    class Meta:
        strict = True


class FollowSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    image = fields.Str()
    following = fields.Bool()
    
    user = fields.Nested('self', exclude=('user',), default=True, load_only=True)

    @pre_load
    def make_user(self, data, **kwargs):
        return data['user']

    @post_dump
    def dump_user(self, data, **kwargs):
        return {'user': data}

    class Meta:
        strict = True


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
followers_schema = FollowSchema(many=True)
