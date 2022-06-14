const app = getApp();
const { me } = app.globalData;

Page({
    data: {
        id: undefined,
        competition_id: undefined,
        //
        team: undefined,
        members: undefined,
        applicants: undefined,
        competition: undefined,
        //
        canEdit: false,
        canApply: false,
        //
        loaded: false,
    },
    onLoad(options) {
        this.setData(options);
        this.fetchData();
    },
    fetchData() {
        const { id, competition_id } = this.data;
        wx.showLoading({ title: "加载中", mask: true });

        const fail = () => wx.hideLoading();
        const done = () => {
            const { team, members, applicants, competition } = this.data;
            if (team && members && applicants && competition) {
                wx.hideLoading();
                this.setData({
                    loaded: true,
                    canEdit: me.is_admin || me.is_superadmin || me.id == team.captain.id,
                    canApply:
                        me.id != team.captain.id &&
                        !members.some(x => x.id == me.id) &&
                        !applicants.some(x => x.id == me.id),
                });
            }
        };

        wx.request({
            url: `http://127.0.0.1:8000/api/competitions/${competition_id}`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            fail: fail,
            success: ({ statusCode, data }) => (statusCode == 200 ? this.setData({ competition: data }, done) : fail()),
        });
        wx.request({
            url: `http://127.0.0.1:8000/api/teams/${id}`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            fail: fail,
            success: ({ statusCode, data }) => (statusCode == 200 ? this.setData({ team: data }, done) : fail()),
        });
        wx.request({
            url: `http://127.0.0.1:8000/api/teams/${id}/members`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            fail: fail,
            success: ({ statusCode, data }) => (statusCode == 200 ? this.setData({ members: data }, done) : fail()),
        });
        wx.request({
            url: `http://127.0.0.1:8000/api/teams/${id}/applicants`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            fail: fail,
            success: ({ statusCode, data }) => (statusCode == 200 ? this.setData({ applicants: data }, done) : fail()),
        });
    },
    onPullDownRefresh() {
        wx.stopPullDownRefresh();
        this.fetchData();
    },
    onApplyTap() {
        const { team } = this.data;
        const fail = () => wx.showModal({ title: "提示", content: "操作失败" });
        const success = () => {
            this.fetchData();
            wx.showModal({ title: "提示", content: "已申请加入，请等待队长同意" });
        };
        wx.request({
            url: `http://127.0.0.1:8000/api/teams/${team.id}/applicants`,
            method: "POST",
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            fail: fail,
            success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
        });
    },
    onMemberTap({ currentTarget }) {
        const { member } = currentTarget.dataset;
        wx.navigateTo({
            url: `../user-main/user-main?userId=${member.id}`,
        });
    },
    onMemberLongTap({ currentTarget }) {
        const { member } = currentTarget.dataset;
        const { team, canEdit } = this.data;
        if (canEdit) {
            wx.showActionSheet({
                itemList: ["删除此队员"],
                success: () => {
                    const fail = () => wx.showModal({ title: "提示", content: "操作失败" });
                    const success = () => {
                        this.fetchData();
                        wx.showModal({ title: "提示", content: "已删除此队员" });
                    };
                    wx.request({
                        url: `http://127.0.0.1:8000/api/teams/${team.id}/members?user_id=${member.id}`,
                        method: "DELETE",
                        header: { Authorization: "Bearer " + wx.getStorageSync("token") },
                        fail: fail,
                        success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
                    });
                },
            });
        }
    },
    onApplicantTap({ currentTarget }) {
        const { applicant } = currentTarget.dataset;
        wx.navigateTo({
            url: `../user-main/user-main?userId=${applicant.id}`,
        });
    },
    onApplicantLongTap({ currentTarget }) {
        const { team } = this.data;
        const { applicant } = currentTarget.dataset;
        wx.showActionSheet({
            itemList: ["同意加入", "拒绝加入"],
            success: ({ tapIndex }) => {
                const approve = tapIndex == 0;
                const fail = () => wx.showModal({ title: "提示", content: "操作失败" });
                const success = () => {
                    this.fetchData();
                    wx.showModal({ title: "提示", content: approve ? "已同意加入" : "已拒绝加入" });
                };
                wx.request({
                    url: `http://127.0.0.1:8000/api/teams/${team.id}/applicants?user_id=${applicant.id}&approve=${approve}`,
                    method: "DELETE",
                    header: { Authorization: "Bearer " + wx.getStorageSync("token") },
                    fail: fail,
                    success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
                });
            },
        });
    },
    onDeleteTap() {
        const { team } = this.data;
        wx.showModal({
            title: "提示",
            content: "将解散并删除队伍",
            success: ({ confirm }) => {
                if (confirm) {
                    const fail = () => wx.showModal({ title: "提示", content: "操作失败" });
                    const success = () =>
                        wx.showModal({
                            title: "提示",
                            content: "已成功解散队伍",
                            success: () => wx.navigateBack({ delta: 1 }),
                        });
                    wx.request({
                        url: `http://127.0.0.1:8000/api/teams/${team.id}`,
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
        const { team } = this.data;
        wx.navigateTo({
            url: `../team-create/team-create?id=${team.id}&name=${team.name}&deadline=${team.deadline}&introduce=${team.introduce}&requirements=${team.requirements}`,
        });
    },
});
