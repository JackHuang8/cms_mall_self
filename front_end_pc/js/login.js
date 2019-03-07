var vm = new Vue({
    el: '#loginform',
    data: {
        host: 'http://127.0.0.1:8000',
        username: '',
        password: '',
        remember: false,

        error_username: false,
        error_pwd: false,

        error_msg: '',    // 提示信息
    },

    methods: {
        // 检查数据
        check_username: function(){
            if (!this.username) {
                this.error_username = true;
                this.error_msg = '请填写用户名';
            } else {
                this.error_username = false;
                this.error_msg = '';
            }
        },
        check_pwd: function(){
            if (!this.password) {
                this.error_msg = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
                this.error_msg = '';
            }
        },

        // 表单提交
        on_submit: function(){
            this.check_username();
            this.check_pwd();

            if (this.error_username === false
                && this.error_pwd === false) {
				//发送登录请求
                data={
                    username:this.username,
                    password:this.password,
                };
                axios.post(this.host+'/authorizations/',data).then(response =>{
                    sessionStorage.clear();
                    localStorage.clear();
                    if(this.remember){
                        localStorage.token=response.data.token;
                        localStorage.user_id=response.data.user_id;
                        localStorage.username=response.data.username;
                    }else {
                        sessionStorage.token=response.data.token;
                        sessionStorage.user_id=response.data.user_id;
                        sessionStorage.username=response.data.username;
                    }
                    alert('登陆成功!');
                    location.href = '/index.html'
                }).catch(error =>{
                    if (error.response.status == 400){
                        this.error_msg = '用户名或密码错误'
                    }else {
                        this.error_msg = '服务器错误'
                    }
                })
            }
        },
    }
});