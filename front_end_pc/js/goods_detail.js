var vm = new Vue({
    el: '#app',
    data: {
        host,
        goods: null,
        recommend_goods: null,

        count: 1,            // 添加到购物车的商品数量
        goods_id: 0,         // 当前显示的商品id

        token:''
    },

    mounted: function() {
        this.goods_id = get_query_string('id');
        this.get_goods_detail(this.goods_id);
        this.get_recommend_goods();
    },

    methods:{
        // 判断用户是否已经登录
        is_login: function() {
            this.token = sessionStorage.token || localStorage.token;
            return this.token !== undefined
        },

        // 获取商品详情数据
        get_goods_detail: function(id) {
			//发送请求
            axios.get(this.host+'/goods/detail/'+id+'/').then(response =>{
                this.goods = response.data
            }).catch(error => {
                alert(error.data)
            })
        },

        // 获取推荐商品
        get_recommend_goods: function () {
			//发送请求
            axios.get(this.host+'/goods/recomment/').then(response => {
                this.recommend_goods = response.data
            }).catch(error =>{
                alert(error.response.data)
            })
        },

        addToCart: function() {
            // 添加商品到购物车
            if (this.is_login()) {  // 已经登录
                //发送登录请求
                var data = {
                    goods_id:this.goods_id,
                    count:this.count,
                    selected:false
                };
                var headers = {headers: {'Authorization': 'JWT ' + this.token}, withCredentials: true};
				axios.post(this.host+'/cart/', data, headers).then(response => {
				    alert('添加购物车成功!');
                }).catch(error =>{
                    alert(error.response.data.msg)
                })
            } else {
                // 如果没有登录,跳转到登录界面,引导用户登录
                window.location.href = 'login.html'
            }
        },

        on_increment: function(){
            // 点击增加购买数量
            this.count ++
        },

        on_decrement: function(){
            // 点击减少购买数量
            if (this.count > 1) {
                this.count--;
            }
        },
    },

    filters: {
        formatDate: function (time) {
            return dateFormat(time, "yyyy-mm-dd");
        },

        formatDate2: function (time) {
            return dateFormat(time, "yyyy-mm-dd HH:MM:ss");
        },
    },
});