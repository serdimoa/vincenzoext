/**
 * Created by serdimoa on 30.01.16.
 */

function getWeekDay(date) {
    var days = ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'];

    return days[date.getDay()];
}

function in_date() {
    var date_in = new Date();
    var min_Day = 1,
        max_Day = 5,
        minHours = 12,
        maxHours = 15,
        inMinutes = 30;
    console.log('in_date');
    if (date_in.getDay() >= min_Day && date_in.getDay() <= max_Day) {
        console.log('in_date 1');

        if (date_in.getHours() >= minHours && date_in.getHours() <= maxHours) {
            console.log('in_date 2');

            if (date_in.getHours() == maxHours) {
                if (date_in.getMinutes() <= inMinutes) {
                    $(".allaboutorder").append("<p style='color:#FF5252;'>Акция.Обед в Vincenzo:<strong>-10%</strong></p>");
                    global_inTime = 10;

                }
            }
            else if(date_in.getHours()<maxHours){
                $(".allaboutorder").append("<p style='color:#FF5252;'>Акция.Обед в Vincenzo:<strong>-10%</strong></p>");
                global_inTime = 10;

            }
        }
    }

}