const app = getApp();

Page({
    data: { excellents: [] },
    onLoad() {
        this.fetchData();
    },
    onPullDownRefresh() {
        wx.stopPullDownRefresh();
        this.fetchData();
    },
    fetchData() {
        wx.showLoading({ title: "加载中", mask: true });
        wx.request({
            url: `http://127.0.0.1:8000/api/excellents/`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    this.setData({ excellents: data });
                }
            },
            complete: () => wx.hideLoading(),
        });
    },
    onExcellentTap({ currentTarget }) {
        const { excellent } = currentTarget.dataset;
        console.log(excellent);
        wx.navigateTo({
            url: `../excellent-create/excellent-create?edit=1&excellentId=${excellent.id}&name=${excellent.name}&captain=${excellent.captain}&members=${excellent.members}&introduce=${excellent.introduce}`,
        });
    },
});
