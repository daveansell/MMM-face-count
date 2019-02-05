"use strict";

Module.register("MMM-face-count", {
  // value must be given for each of the parameters
  defaults: {
    debug: false, // if true, the raw data is printed to stdout
    blankTime: 5
  },

  start: function() {
    this.sendSocketNotification("FACECOUNT_START", this.config);
  },

  socketNotificationReceived: function(notification, payload) {
   console.log("MMM-face-count "+notification+" "+payload.toString());
    this.sendNotification(notification, payload);
  },
});
//# sourceURL=MMM-Simple-Swiper.js
