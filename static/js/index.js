/**
 * @param url m3u8 url
 */
function play_video(url) {
    const dp = new DPlayer({
        container: document.getElementById('dplayer'),
        screenshot: true,
        video: {
            //url: 'C:/Users/admin/Desktop/laba_video/film_00000.ts',
            url: url,
            type: 'hls'
        }
    });
}

function collectURL() {
    const url = $("#laba_url").val();
    if (isURL(url)) {
        $.ajax({
            method: 'POST',
            url: 'http://localhost:5000/find_all_videos',
            data: {
                url: url
            },
            success(data) {
                console.log('data', data)
            }
        })
    } else {
        alert(url + ' 不是一个合法的 URL')
    }
}

function isURL(str_url){
    const strRegex = '^((https|http|ftp|rtsp|mms)?://)'
            +'?(([0-9a-z_!~*().&=+$%-]+: )?[0-9a-z_!~*().&=+$%-]+@)?' //ftp的user@
            + '(([0-9]{1,3}.){3}[0-9]{1,3}' // IP形式的URL- 199.194.52.184
            + '|' // 允许IP和DOMAIN（域名）
            + '([0-9a-z_!~*()-]+.)*' // 域名- www.
            + '([0-9a-z][0-9a-z-]{0,61})?[0-9a-z].' // 二级域名
            + '[a-z]{2,6})' // first level domain- .com or .museum
            + '(:[0-9]{1,4})?' // 端口- :80
            + '((/?)|' // a slash isn't required if there is no file name
            + '(/[0-9a-z_!~*().;?:@&=+$,%#-]+)+/?)$';
    const re=new RegExp(strRegex);
    if (re.test(str_url)){
        return (true);
    }else{
        return (false);
    }
}
