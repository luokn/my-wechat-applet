const app = getApp();
const { me } = app.globalData;

Page({
    /**
     * 页面的初始数据
     */
    data: { competitions: [] },
    onLoad() {
        this.setData({ competitions: me.collections });
    },
    onItemTap({ currentTarget }) {
        const { id } = currentTarget.dataset.competition;
        wx.navigateTo({
            url: `../competition-main/competition-main?id=${id}`,
        });
    },
});
