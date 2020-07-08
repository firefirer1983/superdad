import {postData} from "./app.js"


$(function () {
    $(".btn-add-fav").on("click", (event) => {
        let elm = $(event.target)
        let code = elm.attr("code")
        postData("/favourites/add", {"code": code}).then((res) => {
            $(event.target).prop('disabled', true);
            $(event.target).removeClass("btn-primary")
            $(event.target).text("已收藏")
        })
    })
})