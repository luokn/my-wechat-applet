const app = getApp();

Page({
    data: { teams: [], search: "" },
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
            url: `http://127.0.0.1:8000/api/teams/`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    this.setData({ teams: data });
                }
            },
            complete: () => wx.hideLoading(),
        });
    },
    onTeamTap({ currentTarget }) {
        const { team } = currentTarget.dataset;
        wx.navigateTo({ url: `../team-main/team-main?id=${team.id}&competition_id=${team.competition_id}` });
    },
    onSearchTap() {
        wx.request({
            url: `http://127.0.0.1:8000/api/teams/?search=${this.data.search}`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    this.setData({ teams: data });
                }
            },
        });
    },
});
