const app = getApp();

Page({
    data: {
        id: undefined,
        //
        logo_url: "",
        //
        title: "",
        category: "",
        deadline: "",
        home_page: "",
        organizer: "",
        level: "",
        notice: "",
        members_max: 1,
        description: "",
        extra_credits: true,
        //
        level_id: 0,
        category_id: 0,
        levels: ["国家级", "省市级", "校级"],
        categories: ["兴趣爱好类", "学科学术类", "设计类"],
    },
    onLoad(options) {
        if (options.id) {
            this.setData({ id: options.id });
            this.fetchData();
        } else {
            this.setData({ deadline: new Date().toISOString().split("T")[0] });
        }
    },
    fetchData() {
        const { id } = this.data;
        wx.showLoading({ title: "加载中" });
        wx.request({
            url: `http://127.0.0.1:8000/api/competitions/${id}`,
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            success: ({ statusCode, data }) => {
                if (statusCode == 200) {
                    this.setData({
                        ...data,
                        level_id: this.data.levels.indexOf(data.level),
                        category_id: this.data.categories.indexOf(data.category),
                    });
                }
            },
            complete: () => wx.hideLoading(),
        });
    },
    onExtraCreditsChange({ detail }) {
        this.setData({ extra_credits: detail.value });
    },
    onLogoSelect() {
        wx.chooseMedia({
            mediaType: ["image"],
            success: res => {
                this.setData({ logo_url: res.tempFiles[0].tempFilePath });
            },
        });
    },
    onSubmitTap() {
        const {
            id,
            title,
            logo_url,
            members_max,
            deadline,
            home_page,
            organizer,
            notice,
            description,
            extra_credits,

            level_id,
            category_id,
        } = this.data;

        const fail = () => wx.showModal({ title: "提示", content: "发布竞赛失败" });
        const success = () =>
            wx.showModal({
                title: "提示",
                content: id ? "更新成功" : "已成功创建此竞赛",
                success: () => wx.navigateBack({ delta: 1 }),
            });
        wx.request({
            url: id ? `http://127.0.0.1:8000/api/competitions/${id}` : `http://127.0.0.1:8000/api/competitions/`,
            method: id ? "PUT" : "POST",
            header: { Authorization: "Bearer " + wx.getStorageSync("token") },
            data: {
                title,
                logo_url,
                members_max,
                deadline,
                home_page,
                organizer,
                extra_credits,
                notice,
                description,
                level: this.data.levels[level_id],
                category: this.data.categories[category_id],
            },
            fail: fail,
            success: ({ statusCode }) => (statusCode == 200 ? success() : fail()),
        });
    },
});
