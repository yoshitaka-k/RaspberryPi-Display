$(function(){
  /**
  * Weather
  */
  var setWeather = function(data) {
    let $card = $('.weather-card');
    let $list = $card.find('.weather-card__list');
    $card.find('#weather_date').html(data.dt_text);
    $card.find('#icon').attr('src', data.icon_url);
    $list.find('#weather').html(data.weather_jpn);
    $list.find('#weather_dect').html(data.weather_text);
    $list.find('#temp').html(data.temp + '℃');
    $list.find('#temp_min').html(data.temp_min + '℃');
    $list.find('#temp_max').html(data.temp_max + '℃');
    $list.find('#humidity').html(data.humidity + '%');
    $list.find('#wind').html(data.wind_deg + 'の風、' + data.wind_speed + 'm/s');
  };

  /**
  * Schedule
  */
  var setSchedule = function(data) {
    let $card = $('.schedule-card');
    let $ul = $card.find('.schedule-card__list');
    $ul.html('');
    $.each(data, function(k, v) {
      let $li = $('<li/>')
                  .addClass('mdc-list-item')
                  .html($('<span/>')
                    .addClass('mdc-list-item__text')
                    .append(v)
                    .append($('<span/>')
                      .addClass('mdc-list-item__secondary-text')
                      .html(k)));
      $ul.append($li);
    });
  };

  // WebSocket
  socket = new WebSocket('ws://localhost:8090')
  socket.onmessage = function(e) {
    let data = $.parseJSON(e.data);
    console.log(data);
    setWeather(data.weather);
    setSchedule(data.schedule);
  };

  let weeks = new Array('Sun.', 'Mon.', 'Thu.', 'Wed.', 'Thr.', 'Fri.', 'Sat.');
  let twoDigit = function(num) {
         var digit;
         if (num < 10) digit = "0" + num;
         else digit = num;
         return digit;
  };

  /**
  * Date
  */
  let date = function() {
    let now = new Date();
    let date = now.getFullYear() + '/' +
               twoDigit(now.getMonth() + 1) + '/' +
               twoDigit(now.getDate()) +
               ' ' + weeks[now.getDay()];
    if ($('#date').html() === '') $('#date').html(date);
    if (now.getHours() === 0) $('#date').html(date);
  };
  setInterval(date, 1000);

  /**
  * Time
  */
  let clock = function() {
    let now = new Date();
    let time = twoDigit(now.getHours()) + ':' +
               twoDigit(now.getMinutes()) + ':' +
               twoDigit(now.getSeconds());
    $('#time').html(time);
  };
  setInterval(clock, 1000);
});