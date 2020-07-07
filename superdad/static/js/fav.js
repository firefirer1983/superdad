import {postData} from "./app.js"

$(document).ready(() => {
    $(".btn-add-fav").click((event) => {
        let elm = $(event.target)
        let code = elm.attr("code")
        console.log(code)
        postData("/favourites/add", {"code": code}).then((res) => {
            $(event.target).prop('disabled', true);
            $(event.target).removeClass("btn-primary")
            $(event.target).text("已收藏")
        })
    })
})