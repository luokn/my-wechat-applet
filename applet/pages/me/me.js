const app = getApp();

Page({
    data: { me: null },
    onLoad() {
        this.setData({ me: app.globalData.me });
    },
    onPullDownRefresh() {
        wx.stopPullDownRefresh();
        this.fetchMe();
    },
    fetchMe() {
        const fail = () => wx.removeStorageSync("token");
        const success = me => {
            app.globalData.me = me;
            this.setData({ me });
        };
        wx.request({
            url: "http://127.0.0.1:8000/api/users/me",
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            fail: fail,
            success: ({ statusCode, data }) => (statusCode == 200 ? success(data) : fail()),
        });
    },
    onResumeTap() {
        wx.navigateTo({ url: "../resume-edit/resume-edit" });
    },
    onCompetitionCreateTap() {
        const { me } = this.data;
        if (me.is_admin || me.is_superadmin) {
            wx.navigateTo({ url: "../competition-create/competition-create" });
        } else {
            wx.showModal({ title: "提示", content: "你还不是管理员" });
        }
    },
    onUsersTap() {
        const { me } = this.data;
        if (me.is_admin || me.is_superadmin) {
            wx.navigateTo({ url: "../user-index/user-index" });
        } else {
            wx.showModal({ title: "提示", content: "你还不是管理员" });
        }
    },
    onTeamsTap() {
        const { me } = this.data;
        if (me.is_admin || me.is_superadmin) {
            wx.navigateTo({ url: "../team-index/team-index" });
        } else {
            wx.showModal({ title: "提示", content: "你还不是管理员" });
        }
    },
    onCollectionsTap() {
        wx.navigateTo({ url: "../my-collections/my-collections" });
    },
    onExcellentTap() {
        const { me } = this.data;
        if (me.is_admin || me.is_superadmin) {
            wx.navigateTo({ url: "../excellent-create/excellent-create" });
        } else {
            wx.showModal({ title: "提示", content: "你还不是管理员" });
        }
    },
});
