// pages/team-create/team-create.js
Page({
    data: {
        id: undefined,
        competition_id: undefined,
        //
        name: "",
        introduce: "",
        requirements: "",
        deadline: new Date().toISOString().split("T")[0],
    },

    onLoad(options) {
        this.setData(options);
    },

    onSubmitTap() {
        const fail = () => wx.showModal({ title: "提示", content: "操作失败" });
        const success = () => {
            wx.showModal({
                title: "提示",
                content: "操作成功",
                success: () => wx.navigateBack({ delta: 1 }),
            });
        };
        const { id, competition_id, name, deadline, introduce, requirements } = this.data;
        wx.request({
            url: id
                ? `http://127.0.0.1:8000/api/teams/${id}`
                : `http://127.0.0.1:8000/api/competitions/${competition_id}/teams`,
            method: id ? "PUT" : "POST",
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            data: { name, deadline, introduce, requirements },
            success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
        });
    },
});
