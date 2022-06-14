const app = getApp();

Page({
    data: { code: null, username: "", avatar: "https://www.bojji.cc/static/user.png", fromWechat: false },
    onLoad() {
        if (wx.getStorageSync("token")) {
            this.fetchMe();
        } else {
            wx.login({ success: ({ code }) => this.setData({ code }) });
        }
    },
    fetchMe() {
        const fail = () => wx.removeStorageSync("token");
        const success = me => {
            app.globalData.me = me;
            wx.switchTab({ url: "../competition-index/competition-index" });
        };
        wx.request({
            url: "http://127.0.0.1:8000/api/users/me",
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            fail: fail,
            success: ({ statusCode, data }) => (statusCode == 200 ? success(data) : fail()),
        });
    },
    onGetProfileTap() {
        wx.getUserProfile({
            desc: "将获取微信头像与昵称",
            success: ({ userInfo }) => {
                this.setData({ username: userInfo.nickName, avatar: userInfo.avatarUrl, fromWechat: true });
            },
        });
    },
    onLoginTap() {
        const { code, username, avatar } = this.data;
        if (username.length == 0) {
            wx.showModal({ title: "提示", content: "请填写有效的用户名" });
        } else {
            const fail = () => wx.showModal({ title: "提示", content: "登陆失败" });
            const success = data => {
                wx.setStorageSync("token", data.access_token);
                this.fetchMe();
            };
            wx.showLoading({ title: "加载中", mask: true });
            wx.request({
                url: "http://127.0.0.1:8000/api/login/access-token",
                method: "POST",
                header: { "Content-Type": "application/x-www-form-urlencoded" },
                timeout: 5000,
                data: { code: code, username: username, avatar: avatar, grant_type: "code" },
                fail: fail,
                success: ({ statusCode, data }) => (statusCode == 200 ? success(data) : fail()),
                complete: () => wx.hideLoading(),
            });
        }
    },
});
