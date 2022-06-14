// pages/team-create/team-create.js
Page({
    data: {
        name: "",
        captain: "",
        members: "",
        introduce: "",
        //
        edit: false,
        excellentId: null,
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
        const { name, captain, members, introduce, edit, excellentId } = this.data;
        wx.request({
            url: edit ? `http://127.0.0.1:8000/api/excellents/${excellentId}` : `http://127.0.0.1:8000/api/excellents/`,
            method: edit ? "PUT" : "POST",
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            data: { name, captain, members, introduce },
            success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
        });
    },
});
