const app = getApp();
const { me } = app.globalData;

Page({
    data: {
        id: undefined,
        teams: [],
        comments: [],
        competition: null,
        //
        canDelete: false,
        collected: false,
    },
    onLoad(options) {
        this.setData({ canDelete: me.is_admin || me.is_superadmin });
        console.log(me);
        if (options.id) {
            this.setData({ id: options.id, collected: me.collections.some(x => x.id == options.id) });
            this.fetchData();
        }
    },
    fetchData() {
        const { id } = this.data;
        wx.showLoading({ title: "加载中", mask: true });
        wx.request({
            url: `http://127.0.0.1:8000/api/competitions/${id}`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) this.setData({ competition: data });
            },
            complete: () => wx.hideLoading(),
        });
        wx.request({
            url: `http://127.0.0.1:8000/api/competitions/${id}/teams`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) this.setData({ teams: data });
            },
            complete: () => wx.hideLoading(),
        });
        wx.request({
            url: `http://127.0.0.1:8000/api/competitions/${id}/comments`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) this.setData({ comments: data });
            },
            complete: () => wx.hideLoading(),
        });
    },
    onPullDownRefresh() {
        wx.stopPullDownRefresh();
        this.fetchData();
    },
    onTeamTap({ currentTarget }) {
        const { team } = currentTarget.dataset;
        const { competition } = this.data;
        wx.navigateTo({ url: `../team-main/team-main?id=${team.id}&competition_id=${competition.id}` });
    },
    onJoinTap() {
        const { competition } = this.data;
        wx.navigateTo({
            url: `../team-create/team-create?competition_id=${competition.id}`,
        });
    },
    onDeleteTap() {
        const { competition } = this.data;
        wx.showModal({
            title: "提示",
            content: "将删除竞赛以及所有参赛队伍",
            success: ({ confirm }) => {
                if (confirm) {
                    const fail = () => wx.showModal({ title: "提示", content: "删除失败" });
                    const success = () =>
                        wx.showModal({
                            title: "提示",
                            content: "已成功删除竞赛",
                            success: () => wx.navigateBack({ delta: 1 }),
                        });
                    wx.request({
                        url: `http://127.0.0.1:8000/api/competitions/${competition.id}`,
                        method: "DELETE",
                        header: { Authorization: "Bearer " + wx.getStorageSync("token") },
                        fail: fail,
                        success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
                    });
                }
            },
        });
    },

    onEditTap() {
        const { id } = this.data.competition;
        wx.navigateTo({ url: `../competition-create/competition-create?id=${id}` });
    },

    onCommentTap({ currentTarget }) {
        const { id } = this.data.competition;
        const { comment } = currentTarget.dataset;
        wx.showModal({
            title: comment ? "请输入回复内容" : "请输入评论内容",
            editable: true,
            success: ({ confirm, content }) => {
                if (confirm && content.length != 0) {
                    const fail = () => wx.showModal({ title: "提示", content: "评论失败，请重试" });
                    const success = () => this.fetchData();
                    wx.request({
                        url: comment
                            ? `http://127.0.0.1:8000/api/comments/${comment.id}/replies`
                            : `http://127.0.0.1:8000/api/competitions/${id}/comments/`,
                        method: "POST",
                        header: { Authorization: "Bearer " + wx.getStorageSync("token") },
                        data: { msg: content },
                        fail: fail,
                        success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
                    });
                }
            },
        });
    },
    onCommentPress({ currentTarget }) {
        const { comment } = currentTarget.dataset;
        wx.showModal({
            title: "确认删除此评论吗？",
            success: ({ confirm }) => {
                if (confirm) {
                    const fail = () => wx.showModal({ title: "提示", content: "删除失败" });
                    const success = () => this.fetchData();
                    wx.request({
                        url: `http://127.0.0.1:8000/api/comments/${comment.id}`,
                        method: "DELETE",
                        header: { Authorization: "Bearer " + wx.getStorageSync("token") },
                        fail: fail,
                        success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
                    });
                }
            },
        });
    },
    onCollectTap() {
        const { competition, collected } = this.data;
        wx.request({
            url: `http://127.0.0.1:8000/api/users/me/collections?competition_id=${competition.id}`,
            method: collected ? "DELETE" : "POST",
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode }) => {
                if (statusCode == 200) {
                    this.setData({ collected: !collected });
                    if (collected) {
                        me.collections = me.collections.filter(x => x.id != competition.id);
                    } else {
                        me.collections.push(this.data.competition);
                    }
                }
            },
        });
    },
});
