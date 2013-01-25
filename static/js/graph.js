function Graph(canvasId, graphType, horDataPoints, vertDataPoints, interval, offset){
    this.canvasId = canvasId;
    this.graphType = graphType;
    this.interval = interval;
    this.offset = offset;
    this.horDataPoints = horDataPoints;
    this.vertDataPoints = vertDataPoints;

    this.update();

}

Graph.prototype.paintGrid = function(){
    var ctx = $(this.canvasId).get(0).getContext('2d');

    ctx.beginPath();
    //ctx.rect(0,0,this.width, this.height);

    ctx.rect(this.borderWidth, this.borderHeight, this.graphWidth, this.graphHeight);
    // hor
    ctx.stroke();

    ctx.beginPath();

    ctx.strokeStyle = "#777"
    for (var i=1; i<this.vertDataPoints; i++){
       ctx.moveTo(this.borderWidth, this.borderHeight + i * this.heightUnit)
       ctx.lineTo(this.width - this.borderWidth, this.borderHeight + i * this.heightUnit);
    }     

    // vert
    for (var j=1; j<this.horDataPoints; j++){
       ctx.moveTo(this.widthUnit * (j) + this.borderWidth, this.borderHeight)
       ctx.lineTo(this.widthUnit * (j) + this.borderWidth, this.height - this.borderHeight);
    }  
    
    ctx.stroke();
} 


//Functie die gecalled wordt om het grid te restoren
Graph.prototype.update = function(){
    this.width = $(this.canvasId).parent().width();
    this.height = Math.floor(this.width * 0.7);

    $(this.canvasId).attr('width', this.width).attr('height', this.height);

    this.borderHeight = 0.1 * this.height;
    this.borderWidth = 0.1 * this.width;

    this.graphWidth = (this.width - this.borderWidth*2);
    this.graphHeight =  (this.height - this.borderHeight*2); 

    this.widthUnit = this.graphWidth / (this.horDataPoints-1);
    this.heightUnit = this.graphHeight / (this.vertDataPoints-1);

    this.paintGrid();

    
}

//Functie die gecalled wordt als er een nieuw datapunt opgevraagd moet worden
Graph.prototype.updateData = function(){
    var me = this;

    $.jsonRPC.request('getDataPoints', {
        params: [me.interval, me.horDataPoints, me.offset],
        success: function(result) {
            console.log(result.result);
            me.update();
            me.drawGraph(result.result);
        },
        error: function(result) {
            console.log(result);
        }
    });
}

Graph.prototype.onResize = function(){
    this.update();
    this.drawGraph(this.dataArray);

}

Graph.prototype.drawGraph = function(dataArray){
    this.dataArray = dataArray;
    var ctx = $(this.canvasId).get(0).getContext('2d');

    ctx.strokeStyle = '#f00';
    ctx.lineWidth = 3;
    ctx.beginPath();

    if(dataArray.length > 0){
        var yPos = (this.borderHeight + this.graphHeight) - (dataArray[0] * this.graphHeight);
        ctx.moveTo(this.borderWidth, yPos);
    
        for(var j=1; j<dataArray.length; j++){
            var newyPos = (this.borderHeight + this.graphHeight) - (dataArray[j] * this.graphHeight);
            ctx.lineTo(this.borderWidth + j * this.widthUnit, newyPos);

            
        }
        ctx.stroke();
        
    }

    for(var i=0; i<dataArray.length; i++){
        var yPos = (this.borderHeight + this.graphHeight) - (dataArray[i] * this.graphHeight);
        ctx.beginPath();
        ctx.arc(this.borderWidth + i * this.widthUnit, yPos, this.widthUnit * 0.1, 0, Math.PI * 2);
        ctx.fillStyle = 'green';
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = '#003300';
        ctx.stroke();
    }

}
 
    
/*

        function paintHorizontalLegenda(canvasId){
            var width = $(canvasId).width();
            var height = $(canvasId).height();

            var widthUnit = width / 12;
            var heightUnit = height / 10;

            var ctx = $(canvasId).get(0).getContext('2d')
            ctx.beginPath();
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            for (var i=0; i<=8; i++){
                ctx.fillText((8-i), widthUnit * 0.5, heightUnit * (i+1), widthUnit);
            }

            ctx.stroke();  

        }

        function paintVerticalLegenda(canvasId){
            var width = $(canvasId).width();
            var height = $(canvasId).height();

            var widthUnit = width / 12;
            var heightUnit = height / 10;

            var ctx = $(canvasId).get(0).getContext('2d')
            ctx.beginPath();
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            for (var i=0; i<=10; i++){
                ctx.fillText((i), widthUnit * (i+1), heightUnit * (9.5), widthUnit);
            }

            ctx.stroke();  

        }
*/           
