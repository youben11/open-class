var tag_filters = document.getElementsByClassName('filter-tag');
var time_filters = document.getElementsByClassName('filter-time');
var tag_container = document.getElementById('tag-list');
var tag_filter_front;
var time_filter_front;

var input_value;
var tag_filter_list = [];
var time_filter_list = [];

function search_tag(data) {
    tag_filter_list.push(data)
    ajax()
}

function search_time(data) {
    time_filter_list.push(data);
    ajax()
}

function search_again_tag(data) {
    for (var k = 0; k < tag_filter_list.length; k++) {
        if (tag_filter_list[k] === data){
            tag_filter_list.splice(k, 1);
            k=-1;
        }
    }
    ajax()
}

function search_again_time(data) {
    for (var k = 0; k < time_filter_list.length; k++) {
        if (time_filter_list[k] === data){
            time_filter_list.splice(k, 1);
            k=-1;
        }
    }
    ajax()
}




function search_title() {
    var input = document.getElementById('inlineFormInputGroup');
    input_value=input.value.toLowerCase();
    ajax()
}
