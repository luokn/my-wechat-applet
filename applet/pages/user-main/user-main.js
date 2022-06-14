// pages/user-main/user-main.js
Page({
    data: {
        user: null,
    },
    onLoad: function ({ userId }) {
        wx.request({
            url: `http://127.0.0.1:8000/api/users/${userId}`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    this.setData({ user: data });
                }
            },
        });
    },
});
