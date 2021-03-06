var vm = new Vue({
    el: '#app',
    data: {
        host,
        // 双向绑定变量
        username: '',
        password: '',
        password2: '',
        mobile: '',
        sms_code: '',
        allow: false,

        // 控制元素是否显示
        error_name: false,
        error_password: false,
        error_check_password: false,
        error_phone: false,
        error_sms_code: false,
        error_allow: false,

        // 出错提示
        error_name_message: '请输入5-20个字符的用户名',
        error_password_message: '请输入8-20位的登录密码',
        error_phone_message: '请输入正确的手机号',
        error_sms_code_message: '请输入短信验证码',
        sms_code_tip: '获取验证码',

        // 图片验证码
        image_code_id: '',
        image_code_url: '',
    },

    // 当vue实例挂载到界面后执行, 可以在此方法中执行界面初始化操作
    mounted: function () {
    },

    methods: {
        check_username: function () {
            var len = this.username.length;
            if (len < 5 || len > 20) {
                this.error_name = true;
            } else {
                this.error_name = false;
                axios.get(this.host + '/usernames/' + this.username + '/count/', {responseType: 'json'}).then(response => {
                    if (response.data.count > 0) {
                        this.error_name_message = '用户名已存在';
                        this.error_name = true;
                    }
                }).catch(error => {
                    console.log(error.response.data);
                    this.error_name_message = error.response.data;
                })
            }
        },

        check_pwd: function () {
            var len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },

        check_cpwd: function () {
            if (this.password !== this.password2) {
                this.error_check_password = true;
            } else {
                this.error_check_password = false;
            }
        },

        check_phone: function () {
            var re = /^1[345789]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone = true;
            }
        },

        check_sms_code: function () {
            var len = this.sms_code.length;
            if (len === 0) {
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },

        check_allow: function () {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },

        // 获取短信
        get_sms_code: function () {
            this.check_phone();

            if (!this.error_phone) {
                axios.get(this.host + '/sms_codes/' + this.mobile + '/').then(function (response) {
                    alert(response.data.msg);
                }).catch(function (error) {
                    alert('获取验证码失败')
                })

            }
        },

        // 点击注册按钮
        on_submit: function () {

            this.check_username();
            this.check_pwd();
            this.check_cpwd();
            this.check_phone();
            this.check_allow();
            this.check_sms_code();

            if (this.error_name === false
                && this.error_password === false
                && this.error_check_password === false
                && this.error_phone === false
                && this.error_allow === false
                && this.error_sms_code === false) {
                //发送注册请求
                var data = {
                    username:this.username,
                    password:this.password,
                    password2:this.password2,
                    mobile:this.mobile,
                    sms_code:this.sms_code,
                    allow:this.allow,
                };
                axios.post(this.host+'/users/',data).then(response =>{
                    alert('注册成功');

                    sessionStorage.clear();
                    localStorage.clear();
                    localStorage.token =response.data.token;
                    localStorage.username = response.data.username;
                    localStorage.user_id = response.data.id;

                    location.href = '/index.html';
                }).catch(error =>{
                    alert(error.response.data.non_field_errors)
                })
            } else {
                alert('填写有误')
            }
        },
    }
});

