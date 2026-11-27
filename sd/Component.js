sap.ui.define([
    "sap/ui/core/UIComponent",
    "sap/ui/Device"
], function (UIComponent, Device) {
    "use strict";

    return UIComponent.extend("com.avlis.distribuidora.dashboard.Component", {
        metadata: {
            manifest: "json"
        },

        init: function () {
            // Llamada al init del componente base
            UIComponent.prototype.init.apply(this, arguments);

            // Ajustar densidad de contenido segun dispositivo
            if (!Device.support.touch) {
                document.body.classList.add("sapUiSizeCompact");
            } else {
                document.body.classList.add("sapUiSizeCozy");
            }
        }
    });
});
