const app = getApp();

Page({
    data: {
        degree: "",
        major: "",
        gender: "",
        username: "",
        introduce: "",
        phone_number: "",
        wechat_number: "",
    },
    onLoad() {
        const { degree, major, gender, username, introduce, phone_number, wechat_number } = app.globalData.me;
        this.setData({ degree, major, gender, username, introduce, phone_number, wechat_number });
    },
    onSubmitTap() {
        console.log(this.data);
        const { degree, major, gender, username, introduce, phone_number, wechat_number } = this.data;
        const fail = () => wx.showModal({ title: "提示", content: "更新简历失败" });
        const success = () =>
            wx.showModal({
                title: "提示",
                content: "更新简历成功",
                success: () => wx.navigateBack({ delta: 1 }),
            });
        wx.request({
            url: `http://127.0.0.1:8000/api/users/me`,
            method: "PUT",
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            data: {
                degree,
                major,
                gender,
                username,
                introduce,
                phone_number,
                wechat_number,
            },
            fail: fail,
            success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
        });
    },
});
