var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        token: sessionStorage.token || localStorage.token,

        addresses: [],      // 当前登录用户的地址列表
        user_id: 0,         // 当前登录用户的id
        default_address_id: '',     // 当前登录用户的默认地址的id
    },

    mounted: function(){
        // 请求当前登录用户的所有的地址
        var headers = {headers: {'Authorization': 'JWT ' + this.token}};
       axios.get(this.host+'/addresses/',headers).then(response => {
           this.addresses = response.data.addresses;
           this.user_id = response.data.user_id;
           this.default_address_id = response.data.default_address_id;
       }).catch(error =>{
           alert(error.reponse.data)
       })
    },

    methods: {
        // 设置默认地址
        set_default: function(){
            if (!this.default_address_id) {
                alert('请先选择默认地址');
                return
            }
			//发送请求
            var headers = {headers: {'Authorization': 'JWT ' + this.token}};
           axios.put(this.host+'/addresses/'+this.default_address_id+'/status/',{}, headers).then(response => {
               alert(response.data.msg);
           }).catch(error => {
               alert(error.response.data)
           })
        },

        // 删除地址
        delete_address: function (address_id) {
            // 发送请求
            var headers = {headers: {'Authorization': 'JWT ' + this.token}};
           axios.delete(this.host+'/addresses/'+address_id+'/', headers).then(response => {
               alert('删除成功');
               window.location.href = 'user_center_address.html';
           }).catch(error => {
               alert(error.response.data);
           })
        }
    }
});