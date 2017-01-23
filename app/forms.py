from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField,PasswordField,SubmitField
from wtforms.validators import ValidationError,DataRequired,Length,Required, Email, Regexp, EqualTo
from .models import User

class LoginForm(Form):
    email = StringField('邮箱', validators=[Required(message='邮箱不能为空'), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required(message= '密码不能为空')])
    remember_me = BooleanField('记住登录状态')
    submit = SubmitField('提交')
    
class RegistrationForm(Form):
    email = StringField('邮箱', validators=[Required(message='邮箱不能为空'), Length(1, 64),
                                           Email(message="请输入有效的邮箱地址，比如：username@domain.com")])
    username = StringField('用户名', validators=[
        Required(message= '用户名不能为空'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                          '字母开头且仅允许字母、数字、下划线组成')]) 
    phone = StringField('手机', validators=[Length(0, 11,"不超过11位"), Regexp('^[0-9]*$', 0,
                                          '仅允许数字')]) 
    ###WTForms提供的Regexp验证函数，确保username字段只包含字母，数字，下划线和点号。这个验证函数中的正则表达式后面的两个参数分别是正则表达式的旗标和验证失败时显示的错误消息。
    password = PasswordField('密码', validators=[
        Required(message= '密码不能为空'), EqualTo('password2', message='两次密码必须一致.')]) 
        ###EqualTo验证函数可以验证两个密码字段中的值是否一致，他附属在两个密码字段上，另一个字段作为参数传入。
    password2 = PasswordField('确认密码', validators=[Required(message= '密码不能为空')])
    submit = SubmitField('注册')
    #DataRequired 验证器只是简单地检查相应域提交的数据是否是空。

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱以及被注册.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用.') 
    ###表单类中定义了以validate_开头且后面跟着字段名的方法，这种方法就和常规的验证函数一起调用。
#新增一个用户信息表单
class EditForm(Form):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
