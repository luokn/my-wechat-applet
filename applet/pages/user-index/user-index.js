const app = getApp();
const pages = getCurrentPages();

Page({
    data: { users: [], search: "", select: false },
    onLoad(options) {
        this.setData(options);
        this.fetchData();
    },
    fetchData() {
        wx.showLoading({ title: "加载中", mask: true });
        wx.request({
            url: `http://127.0.0.1:8000/api/users/`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    this.setData({ users: data });
                }
            },
            complete: () => wx.hideLoading(),
        });
    },
    onPullDownRefresh() {
        this.fetchData();
        wx.stopPullDownRefresh();
    },
    onUserTap({ currentTarget }) {
        const { user } = currentTarget.dataset;
        if (this.data.select) {
            let before = pages[pages.length - 2];
            before.onUserSelect(user);
            wx.navigateBack({ delta: 1 });
        } else {
            wx.navigateTo({ url: `../user-main/user-main?userId=${user.id}` });
        }
    },
    //onUserLongTap({ currentTarget }) {
     //   const { me } = app.globalData;
     //  if (!me.is_superadmin) return;
     // const { user } = currentTarget.dataset;
     //   if (user.is_superadmin) return;
     //    wx.showActionSheet({
       //      itemList: [user.is_admin ? "取消该管理员" : "设置为管理员"],
       //  success: () => {
       //         const fail = () => wx.showModal({ title: "提示", content: "操作失败" });
       //         const success = () => {
        //            this.fetchData();
        //            wx.showModal({ title: "提示", content: "操作成功" });
        //       };
         //      wx.request({
         //          url: `http://127.0.0.1:8000/api/users/${user.id}`,
         //          method: "PUT",
        //             header: { Authorization: "Bearer " + wx.getStorageSync("token") },
        //            data: { is_admin: !user.is_admin },
        //             fail: fail,
       //             success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
        //         });
        //     },
     //    });
  //   },
    onSearchTap() {
        wx.request({
            url: `http://127.0.0.1:8000/api/users/?search=${this.data.search}`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    this.setData({ users: data });
                }
            },
        });
    },
});
