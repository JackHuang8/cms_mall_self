var vm = new Vue({
    el: '#app',
    data: {
        host,
        recommend_goods: [],
        categories: [],
    },

    mounted: function () {
        this.get_recommend_goods();
        this.get_category_goods();
    },

    methods: {
		//获取推荐商品
        get_recommend_goods: function () {
           //发送请求
            axios.get(this.host+'/goods/recomment/').then(response => {
                this.recommend_goods = response.data
            }).catch(error => {
                alert(error.response.data)
            })

        },
		//获取分类商品
        get_category_goods: function () {
           //发送请求
            axios.get(this.host+'/goods/category/').then(response => {
                this.categories = response.data
            }).catch(error => {
                alert(error.response.data)
            })
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
