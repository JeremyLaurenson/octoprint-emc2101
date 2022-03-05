/*
 * View model for OctoPrint-Emc2101
 *
 * Author: Jeremy Laurenson
 * License: AGPLv3
 */
$(function() {
    function Emc2101TabViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];
        self.emc2101Model = parameters[0];
        self.use_fahrenheit = ko.observable("");
       
        self.a_name = ko.observable("");
        self.b_name = ko.observable("");
        self.c_name = ko.observable("");
        self.d_name = ko.observable("");
        self.e_name = ko.observable("");
        self.f_name = ko.observable("");
        self.g_name = ko.observable("");
        self.h_name = ko.observable("");
        self.i_name = ko.observable("");
        
        self.a_topspeed = ko.observable("");
        self.b_topspeed = ko.observable("");
        self.c_topspeed = ko.observable("");
        self.d_topspeed = ko.observable("");
        self.e_topspeed = ko.observable("");
        self.f_topspeed = ko.observable("");
        self.g_topspeed = ko.observable("");
        self.h_topspeed = ko.observable("");
        self.i_topspeed = ko.observable("");

        self.a_low_temp  = ko.observable("20");
        self.a_high_temp = ko.observable("30");
        self.b_low_temp  = ko.observable("20");
        self.b_high_temp = ko.observable("30");
        self.c_low_temp  = ko.observable("20");
        self.c_high_temp = ko.observable("30");
        self.d_low_temp  = ko.observable("20");
        self.d_high_temp = ko.observable("30");
        self.e_low_temp  = ko.observable("20");
        self.e_high_temp = ko.observable("30");
        self.f_low_temp  = ko.observable("20");
        self.f_high_temp = ko.observable("30");
        self.g_low_temp  = ko.observable("20");
        self.g_high_temp = ko.observable("30");
        self.h_low_temp  = ko.observable("20");
        self.h_high_temp = ko.observable("30");
        self.i_low_temp  = ko.observable("20");
        self.i_high_temp = ko.observable("30");
        
        self.a_detected = ko.observable("0");
        self.a_temp = ko.observable("0");
        self.a_fanspeed = ko.observable("0");
        self.a_target = ko.observable("0");
        self.b_detected = ko.observable("0");
        self.b_temp = ko.observable("0");
        self.b_fanspeed = ko.observable("0");
        self.b_target = ko.observable("0");
        self.c_detected = ko.observable("0");
        self.c_temp = ko.observable("0");
        self.c_fanspeed = ko.observable("0");
        self.c_target = ko.observable("0");
        self.d_detected = ko.observable("0");
        self.d_temp = ko.observable("0");
        self.d_fanspeed = ko.observable("0");
        self.d_target = ko.observable("0");
        self.e_detected = ko.observable("0");
        self.e_temp = ko.observable("0");
        self.e_fanspeed = ko.observable("0");
        self.e_target = ko.observable("0");
        self.f_detected = ko.observable("0");
        self.f_temp = ko.observable("0");
        self.f_fanspeed = ko.observable("0");
        self.f_target = ko.observable("0");
        self.g_detected = ko.observable("0");
        self.g_temp = ko.observable("0");
        self.g_fanspeed = ko.observable("0");
        self.g_target = ko.observable("0");
        self.h_detected = ko.observable("0");
        self.h_temp = ko.observable("0");
        self.h_fanspeed = ko.observable("0");
        self.h_target = ko.observable("0");
        self.i_detected = ko.observable("0");
        self.i_temp = ko.observable("0");
        self.i_fanspeed = ko.observable("0");
        self.i_target = ko.observable("0");
        
        self.tempGaugeAngle = ko.observable(260);
        self.tempGaugeRadius = ko.observable(77);
        self.tempGaugeOffset = ko.observable(53);
        self.tempGaugeTicks = ko.observableArray([0.0, 0.25, 0.5, 0.75, 1.0]);

        // --- 3/4 Gague Tick code ---
        self.tempGaugeSvgPath = ko.computed(() => {
            a = Math.PI / 180 * (360 - self.tempGaugeAngle()) / 2;
            offset = self.tempGaugeOffset();
            radius = self.tempGaugeRadius();
            leftX = (radius - radius * Math.sin(a) + offset).toFixed(2);
            leftY = (offset + radius + radius * Math.cos(a)).toFixed(2);
            rightX = (2 * radius * Math.sin(a)).toFixed(2);
            rightY = 0;

            return `M${leftX} ${leftY}a${radius} ${radius} 0 1 1 ${rightX} ${rightY}`;
        });
        self.cToF = (celsius) => {
          return celsius * 9 / 5 + 32;
          
        }
        self.tempGaugeLowTickPath = (low,high) => {
            offset=2;
            lotemp=parseFloat(low);
            hitemp=parseFloat(high);
            ticktemp=parseFloat(low);
            if(lotemp>hitemp){
                hitemp=parseFloat(low);
                lotemp=parseFloat(high);
                ticktemp=parseFloat(high);

            }
            hitemp=hitemp+offset;
            lotemp=lotemp-offset;
            ranget=hitemp-lotemp;

            ticktemp=(ticktemp-lotemp)/ranget;
            
            a = Math.PI / 180 * (0.5 * (360 - self.tempGaugeAngle()) + self.tempGaugeAngle() * ticktemp);
            offset = self.tempGaugeOffset();
            radius = self.tempGaugeRadius();
            inset = 10;
            outset = 10;

            innerX = (radius - (radius - inset) * Math.sin(a) + offset).toFixed(2);
            innerY = (offset + radius + (radius - inset) * Math.cos(a)).toFixed(2);
            outerX = (-(inset + outset) * Math.sin(a)).toFixed(2);
            outerY = ((inset + outset) * Math.cos(a)).toFixed(2);

            return `M${innerX} ${innerY}l${outerX} ${outerY}`;
        };

        self.tempGaugeHighTickPath = (low,high) => {
            offset=2;
            lotemp=parseFloat(low);
            hitemp=parseFloat(high);
            ticktemp=parseFloat(high);
            if(lotemp>hitemp){
                hitemp=parseFloat(low);
                lotemp=parseFloat(high);
                ticktemp=parseFloat(low);

            }
            hitemp=hitemp+offset;
            lotemp=lotemp-offset;
            ranget=hitemp-lotemp;

            ticktemp=(ticktemp-lotemp)/ranget;
            
            a = Math.PI / 180 * (0.5 * (360 - self.tempGaugeAngle()) + self.tempGaugeAngle() * ticktemp);
            offset = self.tempGaugeOffset();
            radius = self.tempGaugeRadius();
            inset = 10;
            outset = 10;

            innerX = (radius - (radius - inset) * Math.sin(a) + offset).toFixed(2);
            innerY = (offset + radius + (radius - inset) * Math.cos(a)).toFixed(2);
            outerX = (-(inset + outset) * Math.sin(a)).toFixed(2);
            outerY = ((inset + outset) * Math.cos(a)).toFixed(2);

            return `M${innerX} ${innerY}l${outerX} ${outerY}`;
        };
        self.tempGaugeLowTickTextX = (low,high) => {
            offset=2;
            lotemp=parseFloat(low);
            hitemp=parseFloat(high);
            ticktemp=parseFloat(low);
            if(lotemp>hitemp){
                hitemp=parseFloat(low);
                lotemp=parseFloat(high);
                ticktemp=parseFloat(high);

            }
            hitemp=hitemp+offset;
            lotemp=lotemp-offset;
            ranget=hitemp-lotemp;

            tick=(ticktemp-lotemp)/ranget;
            

            a = Math.PI / 180 * (0.5 * (360 - self.tempGaugeAngle()) + self.tempGaugeAngle() * tick);
            offset = self.tempGaugeOffset();
            radius = self.tempGaugeRadius();
            textOutset = 35;

            textX = (radius - (radius + textOutset) * Math.sin(a) + offset).toFixed(2);

            return textX;
        };

        self.tempGaugeLowTickTextY = (low,high) => {
            offset=2;
            lotemp=parseFloat(low);
            hitemp=parseFloat(high);
            ticktemp=parseFloat(low);
            if(lotemp>hitemp){
                hitemp=parseFloat(low);
                lotemp=parseFloat(high);
                ticktemp=parseFloat(high);

            }
            hitemp=hitemp+offset;
            lotemp=lotemp-offset;
            ranget=hitemp-lotemp;

            tick=(ticktemp-lotemp)/ranget;
            
            
            a = Math.PI / 180 * (0.5 * (360 - self.tempGaugeAngle()) + self.tempGaugeAngle() * tick);
            offset = self.tempGaugeOffset();
            radius = self.tempGaugeRadius();
            textOutset = 35;

            textY = (offset + radius + (radius + textOutset) * Math.cos(a)).toFixed(2);

            return textY;
        };

        self.tempGaugeHighTickTextX = (low,high) => {
            offset=2;
            lotemp=parseFloat(low);
            hitemp=parseFloat(high);
            ticktemp=parseFloat(high);
            if(lotemp>hitemp){
                hitemp=parseFloat(low);
                lotemp=parseFloat(high);
                ticktemp=parseFloat(low);

            }
            hitemp=hitemp+offset;
            lotemp=lotemp-offset;
            ranget=hitemp-lotemp;

            tick=(ticktemp-lotemp)/ranget;
            

            a = Math.PI / 180 * (0.5 * (360 - self.tempGaugeAngle()) + self.tempGaugeAngle() * tick);
            offset = self.tempGaugeOffset();
            radius = self.tempGaugeRadius();
            textOutset = 35;

            textX = (radius - (radius + textOutset) * Math.sin(a) + offset).toFixed(2);

            return textX;
        };

        self.tempGaugeHighTickTextY = (low,high) => {
            offset=2;
            lotemp=parseFloat(low);
            hitemp=parseFloat(high);
            ticktemp=parseFloat(high);
            if(lotemp>hitemp){
                hitemp=parseFloat(low);
                lotemp=parseFloat(high);
                ticktemp=parseFloat(low);

            }
            hitemp=hitemp+offset;
            lotemp=lotemp-offset;
            ranget=hitemp-lotemp;

            tick=(ticktemp-lotemp)/ranget;
            
            
            a = Math.PI / 180 * (0.5 * (360 - self.tempGaugeAngle()) + self.tempGaugeAngle() * tick);
            offset = self.tempGaugeOffset();
            radius = self.tempGaugeRadius();
            textOutset = 35;

            textY = (offset + radius + (radius + textOutset) * Math.cos(a)).toFixed(2);

            return textY;
        };

        
        self.formatTempText = function (temperature) {
             if(self.use_fahrenheit()==true)
            return self.cToF(Number.parseFloat(temperature)).toFixed(1) + "°F";
            else
            return Number.parseFloat(temperature).toFixed(1)+ "°C";

        }
        
        self.formatFanText = function (fanSpeed) {
            if (isNaN(fanSpeed))
                return "Off";
            if (fanSpeed == 0)
                return "Off";
            return Number.parseFloat(fanSpeed).toFixed(1) + "%";
        }
        
        self.formatFanSpeedText = function (fanSpeed) {
            if (isNaN(fanSpeed))
                return "Off";
            if (fanSpeed <100)
                return "Off";
            return Number.parseFloat(fanSpeed).toFixed(0);
        }
        
        self.tempGaugePathLen = ko.computed(() => {
            return (self.tempGaugeRadius() * Math.PI * self.tempGaugeAngle() / 180).toFixed(2);
        });
        self.formatFanOffset = function (fanSpeedR,topSpeed) {
            // Fans operate ususally from 600RPM to around 1900 RPM
            fanSpeed=parseFloat(fanSpeedR); // This gives an RPM.
            fanSpeed=fanSpeed*100/topSpeed; // Closer to a percentage
            if(fanSpeed>100)fanSpeed=100;
            if(fanSpeed<0)fanSpeed=0;
            if (fanSpeed && !isNaN(fanSpeed)) {
                return (self.tempGaugePathLen() * (1 - fanSpeed / 100)).toFixed(2);
            } else return (self.tempGaugePathLen() * 0.001);
        };
        self.formatTempOffset = function (tempR) {
            temp=parseFloat(tempR); // This gives an RPM.
            temp=temp/3;; // 300 degrees tops
            if(temp>100)temp=100;
            if(temp<0)temp=0;
            if (temp && !isNaN(temp)) {
                return (self.tempGaugePathLen() * (1 - temp / 100)).toFixed(2);
            } else return (self.tempGaugePathLen() * 0.001);
        };
        self.formatDetailedTempOffset = function (tempR,tempLow,tempHigh) {
            offset=2;
            lotemp=parseFloat(tempLow);
            hitemp=parseFloat(tempHigh);
            if(lotemp>hitemp){
                hitemp=parseFloat(tempLow);
                lotemp=parseFloat(tempHigh);
            }
            hitemp=hitemp+offset;
            lotemp=lotemp-offset;
            
            temp=parseFloat(tempR);
            temp=(temp-lotemp)*100/(hitemp-lotemp);
            if(temp>100)temp=100;
            if(temp<0)temp=0;
            if (temp && !isNaN(temp)) {
                return (self.tempGaugePathLen() * (1 - temp / 100)).toFixed(2);
            } else return (self.tempGaugePathLen() * 0.01);
        };
        self.formatTargetOffset = function (temp) {
            if(temp>100)temp=100;
            if(temp<1)temp=1;
            if (temp && !isNaN(temp)) {
                return (self.tempGaugePathLen() * (1 - temp / 100)).toFixed(2);
            } else return (self.tempGaugePathLen() * 0.01);
        };

        self.tempGaugeViewBox = ko.computed(() => {
            return `0 0 ${2 * (self.tempGaugeRadius() + self.tempGaugeOffset())} ${2 * (self.tempGaugeRadius() + self.tempGaugeOffset())}`;
        });
        
        self.gaugesCentreInGrid = function (type, index = 0, css = {}) {
            var last = [{}];
            var totalNum = 1;
          
                css.centreInGrid2 = false;
                css.centreInGrid1 = false;
                // Check that this gauge is one of the two in the final row
                if (totalNum == 2 && ((type == last[0].type && index == last[0].index) || (type == last[1].type && index == last[1].index)))
                    css.centreInGrid2 = true;
                // Check that this gauge is the one in the final row
                if (totalNum == 1 && type == last[0].type && index == last[0].index)
                    css.centreInGrid1 = true;

            return css;
        }

        
        self.onBeforeBinding = function () {
            //self.settings = self.global_settings.settings.plugins.emc2101;
        };
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "emc2101") {
                return;
            };
            
            self.use_fahrenheit(false);
            if(data.use_fahrenheit)self.use_fahrenheit(data.use_fahrenheit);
            if (data.a_name)self.a_name(data.a_name);
            if (data.b_name)self.b_name(data.b_name);
            if (data.c_name)self.c_name(data.c_name);
            if (data.d_name)self.d_name(data.d_name);
            if (data.e_name)self.e_name(data.e_name);
            if (data.f_name)self.f_name(data.f_name);
            if (data.g_name)self.g_name(data.g_name);
            if (data.h_name)self.h_name(data.h_name);
            if (data.i_name)self.i_name(data.i_name);


            if (data.a_topspeed)self.a_topspeed(data.a_topspeed);
            if (data.b_topspeed)self.b_topspeed(data.b_topspeed);
            if (data.c_topspeed)self.c_topspeed(data.c_topspeed);
            if (data.d_topspeed)self.d_topspeed(data.d_topspeed);
            if (data.e_topspeed)self.e_topspeed(data.e_topspeed);
            if (data.f_topspeed)self.f_topspeed(data.f_topspeed);
            if (data.g_topspeed)self.g_topspeed(data.g_topspeed);
            if (data.h_topspeed)self.h_topspeed(data.h_topspeed);
            if (data.i_topspeed)self.i_topspeed(data.i_topspeed);

            if(data.a_low_temp) self.a_low_temp( data.a_low_temp);
            if(data.a_high_temp)self.a_high_temp(data.a_high_temp);
            if(data.b_low_temp) self.b_low_temp( data.b_low_temp);
            if(data.b_high_temp)self.b_high_temp(data.b_high_temp);
            if(data.c_low_temp) self.c_low_temp( data.c_low_temp);
            if(data.c_high_temp)self.c_high_temp(data.c_high_temp);
            if(data.d_low_temp) self.d_low_temp( data.d_low_temp);
            if(data.d_high_temp)self.d_high_temp(data.d_high_temp);
            if(data.e_low_temp) self.e_low_temp( data.e_low_temp);
            if(data.e_high_temp)self.e_high_temp(data.e_high_temp);
            if(data.f_low_temp) self.f_low_temp( data.f_low_temp);
            if(data.f_high_temp)self.f_high_temp(data.f_high_temp);
            if(data.g_low_temp) self.g_low_temp( data.g_low_temp);
            if(data.g_high_temp)self.g_high_temp(data.g_high_temp);
            if(data.h_low_temp) self.h_low_temp( data.h_low_temp);
            if(data.h_high_temp)self.h_high_temp(data.h_high_temp);
            if(data.i_low_temp) self.i_low_temp( data.i_low_temp);
            if(data.i_high_temp)self.i_high_temp(data.i_high_temp);
        
            
            if (data.a_detected)self.a_detected(data.a_detected);
            if (data.a_temp)self.a_temp(data.a_temp);
            if (data.a_fanspeed)self.a_fanspeed(data.a_fanspeed);
            if (data.a_target)self.a_target(data.a_target);

            if (data.b_detected)self.b_detected(data.b_detected);
            if (data.b_temp)self.b_temp(data.b_temp);
            if (data.b_fanspeed)self.b_fanspeed(data.b_fanspeed);
            if (data.b_target)self.b_target(data.b_target);

            if (data.c_detected)self.c_detected(data.c_detected);
            if (data.c_temp)self.c_temp(data.c_temp);
            if (data.c_fanspeed)self.c_fanspeed(data.c_fanspeed);
            if (data.c_target)self.c_target(data.c_target);

            if (data.d_detected)self.d_detected(data.d_detected);
            if (data.d_temp)self.d_temp(data.d_temp);
            if (data.d_fanspeed)self.d_fanspeed(data.d_fanspeed);
            if (data.d_target)self.d_target(data.d_target);

            if (data.e_detected)self.e_detected(data.e_detected);
            if (data.e_temp)self.e_temp(data.e_temp);
            if (data.e_fanspeed)self.e_fanspeed(data.e_fanspeed);
            if (data.e_target)self.e_target(data.e_target);

            if (data.f_detected)self.f_detected(data.f_detected);
            if (data.f_temp)self.f_temp(data.f_temp);
            if (data.f_fanspeed)self.f_fanspeed(data.f_fanspeed);
            if (data.f_target)self.f_target(data.f_target);

            if (data.g_detected)self.g_detected(data.g_detected);
            if (data.g_temp)self.g_temp(data.g_temp);
            if (data.g_fanspeed)self.g_fanspeed(data.g_fanspeed);
            if (data.g_target)self.g_target(data.g_target);

            if (data.h_detected)self.h_detected(data.h_detected);
            if (data.h_temp)self.h_temp(data.h_temp);
            if (data.h_fanspeed)self.h_fanspeed(data.h_fanspeed);
            if (data.h_target)self.h_target(data.h_target);

            if (data.i_detected)self.i_detected(data.i_detected);
            if (data.i_temp)self.i_temp(data.i_temp);
            if (data.i_fanspeed)self.i_fanspeed(data.i_fanspeed);
            if (data.i_target)self.i_target(data.i_target);

        // TODO: Implement your plugin's view model here.
        }
    }
    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: Emc2101TabViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [  ],
        // Elements to bind to, e.g. #settings_plugin_emc2101, #tab_plugin_emc2101, ...
        elements: [  "#tab_plugin_emc2101"  ]
    });
});
