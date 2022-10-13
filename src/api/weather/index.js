import request from "@/request";
export const getWeatherList = param =>request({
    url:'v1/list',
    param
})
export const getWeather = name =>request({
    url:`v1/weather?name=${name}`,
})
export const getWeatherDetails = name =>request({
    url:`v1/weatherDetails?name=${name}`,
})
export const gdWeatherCode = code =>request({
    url:`v1/gdWeather?code=${code}`,
})
