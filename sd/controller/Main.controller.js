sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/m/MessageToast",
    "sap/m/MessageBox"
], function (Controller, JSONModel, MessageToast, MessageBox) {
    "use strict";

    return Controller.extend("com.avlis.distribuidora.dashboard.controller.Main", {

        onInit: function () {
            // Guardar referencia global para callbacks desde HTML
            window.dashboardController = this;

            // Modelo inicial con los datos del centro de mando
            var oData = {
                kpi: {
                    salesOrders: "2,357",
                    quotations: "1,288",
                    deliveries: "2,058",
                    billingDocs: "1,969",
                    partners: "323",
                    priceConditions: "12",
                    materialDocs: "4,534",
                    warehouseOrders: "789"
                },
                meta: {
                    lastUpdatedText: this._getFormattedTimestamp()
                }
            };

            var oModel = new JSONModel(oData);
            this.getView().setModel(oModel);
        },

        /**
         * Manejador de clic en tarjetas KPI
         * @param {string} sSemanticObject Objeto Semantico (ej. SalesOrder)
         * @param {string} sAction Accion (ej. create, manage)
         * @param {string} sLabel Descripcion amigable de la transaccion
         */
        onKpiCardPress: function (sSemanticObject, sAction, sLabel) {
            this._navigateToFioriIntent(sSemanticObject, sAction, sLabel);
        },

        /**
         * Manejador de botones de accion rapida superior
         */
        onQuickActionPress: function (sSemanticObject, sAction) {
            var sLabel = sSemanticObject === "SalesOrder" ? "VA01 - Crear Pedido de Ventas" : "VL01N - Crear Entrega de Salida";
            this._navigateToFioriIntent(sSemanticObject, sAction, sLabel);
        },

        /**
         * Logica de navegacion por Intencion en SAP Fiori Launchpad / Work Zone
         */
        _navigateToFioriIntent: function (sSemanticObject, sAction, sLabel) {
            var that = this;
            var oCrossAppNavigator = sap.ushell && sap.ushell.Container && sap.ushell.Container.getService("CrossApplicationNavigation");

            if (oCrossAppNavigator) {
                // Ejecucion dentro del Portal Fiori / SAP Build Work Zone
                oCrossAppNavigator.toExternal({
                    target: {
                        semanticObject: sSemanticObject,
                        action: sAction
                    }
                });
            } else {
                // Modo Standalone / Vista previa local en navegador
                MessageToast.show("Abriendo en S/4HANA: " + sLabel + "\nIntent: #" + sSemanticObject + "-" + sAction, {
                    duration: 3500,
                    width: "25em"
                });
            }
        },

        /**
         * Refrescar metricas en tiempo real
         */
        onRefresh: function () {
            var oModel = this.getView().getModel();
            var oData = oModel.getData();

            // Simulacion de incremento en vivo de pedidos
            var currentOrders = parseInt(oData.kpi.salesOrders.replace(",", ""), 10);
            oData.kpi.salesOrders = (currentOrders + 1).toLocaleString();
            oData.meta.lastUpdatedText = this._getFormattedTimestamp();

            oModel.setData(oData);

            MessageToast.show("Datos sincronizados en vivo con S/4HANA 1909 (Cliente 100)", {
                duration: 2500
            });
        },

        _getFormattedTimestamp: function () {
            var now = new Date();
            var hours = String(now.getHours()).padStart(2, '0');
            var minutes = String(now.getMinutes()).padStart(2, '0');
            var seconds = String(now.getSeconds()).padStart(2, '0');
            return "Datos en vivo desde S/4HANA 1909 (Cliente 100) · Actualizado a las " + hours + ":" + minutes + ":" + seconds + " · AVLIS Consultores";
        }
    });
});
