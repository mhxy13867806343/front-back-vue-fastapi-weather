

const network = function(options) {
    let data = {};
    if (options.data) {
        data = options.data;
    }
    /* 请求头设置 */
    let header={
    };
    return new Promise((resolve,reject)=>{
        let url=process.uniEnv.BASE_API + options.url;
        uni.request({
            url:url,
            method:options.method || 'GET',
            dataType:'json',
            header:header,
            data,
            param:data,
            success:(res)=>{
                resolve(res.data);
            },
            fail:(err)=>{
                uni.hideLoading();
                reject(err);
            }
        });
    })
}

export default network;
