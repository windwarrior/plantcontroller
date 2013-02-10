function Slider(sliderId){
    this.sliderId = sliderId;
    this.redWidth = 0.20;
    this.yellowWidth = 0.33;
    this.greenWidth = 0.47;

    console.log("Hoihoi");

    $(this.sliderId).css('width', '100%');

    $(this.sliderId).append('<div class="red"></div><div class="yellow"></div><div class="green"></div>');

    $(this.sliderId + ' *').css('float', 'left');
    $(this.sliderId + ' *').css('height', '20px');
    
    $(this.sliderId + ' .red').css('width', this.redWidth*100  + '%');
    $(this.sliderId + ' .red').css('background-color', 'red');

    $(this.sliderId + ' .yellow').css('width', this.yellowWidth*100  + '%');
    $(this.sliderId + ' .yellow').css('background-color', 'yellow');

    $(this.sliderId + ' .green').css('width',  this.greenWidth*100 + '%');
    $(this.sliderId + ' .green').css('background-color','green');
}

Slider.prototype.resize = function(){

    this.width = $(this.sliderId).width;
    

}

