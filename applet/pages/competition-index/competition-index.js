const app = getApp();
const { me } = app.globalData;

Page({
    data: { competitions: [], all_competitions: [], search: "" },

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
            url: `http://127.0.0.1:8000/api/competitions/`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    const competitions = this.preproc(data);

                    var collections = [];
                    competitions.forEach(c => {
                        if (me.collections.some(x => x.id == c.id)) {
                            collections.push(c);
                        }
                    });

                    me.collections = collections;

                    this.setData({ competitions, all_competitions: competitions });
                }
            },
            complete: () => wx.hideLoading(),
        });
    },

    onSearchTap() {
        wx.request({
            url: `http://127.0.0.1:8000/api/competitions/?search=${this.data.search}`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    const competitions = this.preproc(data);
                    this.setData({ competitions, all_competitions: competitions });
                }
            },
        });
    },

    onItemTap({ currentTarget }) {
        const { id } = currentTarget.dataset.competition;
        wx.navigateTo({
            url: `../competition-main/competition-main?id=${id}`,
        });
    },

    onCategoryTap({ currentTarget }) {
        const { category } = currentTarget.dataset;
        this.setData({ competitions: this.data.all_competitions.filter(x => x.category == category) });
    },

    onStateTap({ currentTarget }) {
        const { state } = currentTarget.dataset;
        this.setData({ competitions: this.data.all_competitions.filter(x => x.state == state) });
    },

    preproc(competitions) {
        const now = Date.now();
        const day = 1000 * 3600 * 24;

        competitions.forEach(x => {
            const deadline = Date.parse(x["deadline"]) + 1 * day;
            if (deadline - now > 5 * day) {
                x["state"] = "正在报名";
            } else {
                x["state"] = deadline > now ? "即将截止" : "报名截止";
            }
        });
        return competitions;
    },
});
