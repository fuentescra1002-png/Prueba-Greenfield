// =========================================================================
// MAESTRO DE DATOS REALES SAP EWM (ALMACÉN Z101 · SOCIEDAD ZX01 · CENTRO ZC10)
// Greenfield Distribuidora Express S.A. · Probado en S/4HANA Mandante 100
// =========================================================================

window.ewmMasterData = {
    warehouse: "Z101",
    center: "ZC10",
    company: "ZX01",
    purchasingOrg: "ZX01",
    purchasingGroup: "ZX1",
    
    // Proveedores Homologados
    vendors: [
        { id: "17300096", name: "Oleo-North Oils & Logistics LLC", country: "US", city: "Houston, TX", terms: "NT30" },
        { id: "17300001", name: "AgroExpress Commodities S.A.", country: "US", city: "Chicago, IL", terms: "NT30" },
        { id: "10300001", name: "Distribuidora Mayorista Central", country: "US", city: "Miami, FL", terms: "NT00" }
    ],

    // Materiales del Negocio
    materials: [
        { id: "ZMAT-02", desc: "Aceite Vegetal Premium (Caja x 12)", baseUom: "CJ", weight: "11.5 KG", huType: "ZPL-120", fastMover: true },
        { id: "ZMAT-01", desc: "Harina de Trigo Panadera (Saco 25kg)", baseUom: "SC", weight: "25.0 KG", huType: "ZPL-120", fastMover: true },
        { id: "ZMAT-03", desc: "Arroz Grano Largo Especial (Bolsa 50kg)", baseUom: "BL", weight: "50.0 KG", huType: "ZPL-120", fastMover: false },
        { id: "ZMAT-04", desc: "Azúcar Blanco Refinado (Bulto 50kg)", baseUom: "BL", weight: "50.0 KG", huType: "ZPL-120", fastMover: false },
        { id: "ZMAT-05", desc: "Manteca Vegetal Industrial (Caja 15kg)", baseUom: "CJ", weight: "15.0 KG", huType: "ZPL-120", fastMover: false },
        { id: "TG11", desc: "Trading Goods 11 (Comercial Estándar S4H)", baseUom: "PI", weight: "1.2 KG", huType: "ZPL-120", fastMover: false }
    ],

    // Materiales de Embalaje (Handling Units)
    packagingMaterials: [
        { id: "ZPL-120", desc: "Pallet Estándar Europeo 1200x800mm Madera", maxWeight: "1200 KG", tare: "25 KG" },
        { id: "ZPL-100", desc: "Pallet Americano Industrial 1200x1000mm", maxWeight: "1500 KG", tare: "28 KG" },
        { id: "ZBX-001", desc: "Caja Máster Contenedora Corrugada", maxWeight: "50 KG", tare: "1.2 KG" }
    ],

    // Clases de Proceso de Almacén (WPT)
    processTypes: [
        { code: "Z011", desc: "Entrada en Ubicación Pallet HU Estándar (Putaway)", storageType: "Z020" },
        { code: "Z010", desc: "Recepción Directa en Playa de Muelle", storageType: "Z910" },
        { code: "Z020", desc: "Picking Saliente para Despacho SD", storageType: "Z030" },
        { code: "Z030", desc: "Reabastecimiento Interno Rack -> Picking", storageType: "Z030" },
        { code: "Z040", desc: "Traspaso de Depósito ZR01 -> ZA01 (Mov. 411)", storageType: "Z020" }
    ],

    // Tipos de Almacén EWM en Z101
    storageTypes: [
        { id: "Z910", name: "Playa de Entrada / Puesta a Disposición (Inbound Staging)", bins: 8, role: "Staging Area" },
        { id: "Z020", name: "Estanterías Racks Paletizados (High-Bay Storage)", bins: 48, role: "Standard Racks" },
        { id: "Z030", name: "Zona Picking Manual y Fraccionamiento", bins: 24, role: "Fast Picking" },
        { id: "Z920", name: "Playa de Salida / Despacho Camiones (Outbound Staging)", bins: 8, role: "Outbound Area" }
    ],

    // Ubicaciones de Almacén (Storage Bins)
    storageBins: [
        { bin: "GR-ZD01", type: "Z910", section: "ZS01", desc: "Muelle 01 - Recepción Descarga", status: "Occupied", huCount: 2 },
        { bin: "GR-ZD02", type: "Z910", section: "ZS01", desc: "Muelle 02 - Recepción Descarga", status: "Available", huCount: 0 },
        { bin: "RACK-01-A-01", type: "Z020", section: "0001", desc: "Pasillo A - Rack 01 Nivel 1", status: "Occupied", huCount: 1, mat: "ZMAT-02", qty: 50 },
        { bin: "RACK-01-A-02", type: "Z020", section: "0001", desc: "Pasillo A - Rack 01 Nivel 2", status: "Occupied", huCount: 1, mat: "ZMAT-02", qty: 50 },
        { bin: "RACK-01-A-03", type: "Z020", section: "0001", desc: "Pasillo A - Rack 01 Nivel 3", status: "Available", huCount: 0 },
        { bin: "RACK-01-A-04", type: "Z020", section: "0001", desc: "Pasillo A - Rack 01 Nivel 4", status: "Available", huCount: 0 },
        { bin: "RACK-02-A-01", type: "Z020", section: "0001", desc: "Pasillo A - Rack 02 Nivel 1", status: "Occupied", huCount: 1, mat: "ZMAT-01", qty: 40 },
        { bin: "RACK-02-A-02", type: "Z020", section: "0001", desc: "Pasillo A - Rack 02 Nivel 2", status: "Available", huCount: 0 },
        { bin: "RACK-03-B-01", type: "Z020", section: "0002", desc: "Pasillo B - Rack 03 Nivel 1", status: "Occupied", huCount: 1, mat: "ZMAT-03", qty: 30 },
        { bin: "RACK-03-B-02", type: "Z020", section: "0002", desc: "Pasillo B - Rack 03 Nivel 2", status: "Available", huCount: 0 },
        { bin: "PICK-01-01", type: "Z030", section: "0001", desc: "Puesto de Picking Suelto Aceites", status: "Occupied", huCount: 1, mat: "ZMAT-02", qty: 15 },
        { bin: "OUT-ZD01", type: "Z920", section: "ZS02", desc: "Muelle 03 - Salida y Carga Camiones", status: "Available", huCount: 0 }
    ],

    // Unidades de Manipulación (HU) activas en el almacén
    handlingUnits: [
        { huId: "1000845920", packMat: "ZPL-120", mat: "ZMAT-02", matDesc: "Aceite Vegetal Premium", qty: 50, uom: "CJ", weight: "575 KG", bin: "GR-ZD01", status: "En Muelle (Pte. Ubicar)", poRef: "4500012891", ibdRef: "180004521" },
        { huId: "1000845921", packMat: "ZPL-120", mat: "ZMAT-02", matDesc: "Aceite Vegetal Premium", qty: 50, uom: "CJ", weight: "575 KG", bin: "RACK-01-A-01", status: "Ubicado en Rack (Disponible)", poRef: "4500012880", ibdRef: "180004510" },
        { huId: "1000845922", packMat: "ZPL-120", mat: "ZMAT-01", matDesc: "Harina de Trigo Panadera", qty: 40, uom: "SC", weight: "1000 KG", bin: "RACK-02-A-01", status: "Ubicado en Rack (Disponible)", poRef: "4500012875", ibdRef: "180004505" },
        { huId: "1000845923", packMat: "ZPL-120", mat: "ZMAT-03", matDesc: "Arroz Grano Largo Especial", qty: 30, uom: "BL", weight: "1500 KG", bin: "RACK-03-B-01", status: "Ubicado en Rack (Disponible)", poRef: "4500012860", ibdRef: "180004490" }
    ],

    // Tareas de Almacén (Warehouse Tasks - WT)
    warehouseTasks: [
        { wtNum: "10000451", procType: "Z011", huId: "1000845920", mat: "ZMAT-02", qty: 50, uom: "CJ", srcBin: "GR-ZD01", destBin: "RACK-01-A-04", status: "Abierta", createdOn: "02.11.2026 10:15", user: "USEREWME" },
        { wtNum: "10000450", procType: "Z011", huId: "1000845921", mat: "ZMAT-02", qty: 50, uom: "CJ", srcBin: "GR-ZD01", destBin: "RACK-01-A-01", status: "Confirmada", createdOn: "02.11.2026 09:30", user: "USER02" },
        { wtNum: "10000449", procType: "Z011", huId: "1000845922", mat: "ZMAT-01", qty: 40, uom: "SC", srcBin: "GR-ZD01", destBin: "RACK-02-A-01", status: "Confirmada", createdOn: "01.11.2026 16:45", user: "USER02" },
        { wtNum: "10000448", procType: "Z020", huId: "1000845915", mat: "ZMAT-02", qty: 20, uom: "CJ", srcBin: "RACK-01-A-02", destBin: "OUT-ZD01", status: "Confirmada", createdOn: "01.11.2026 14:10", user: "USEREWME" }
    ],

    // Historial de Documentos de Compra y Recepción
    inboundHistory: [
        { poNum: "4500012891", poDate: "02.11.2026", vendor: "17300096", vendorName: "Oleo-North Oils", ibdNum: "180004521", mat: "ZMAT-02", qty: 100, uom: "CJ", grStatus: "Contabilizado (101)", putawayStatus: "En Proceso (Z011)", stockLoc: "ZR01", qrfcQueue: "OK (Verde)" },
        { poNum: "4500012880", poDate: "02.11.2026", vendor: "17300096", vendorName: "Oleo-North Oils", ibdNum: "180004510", mat: "ZMAT-02", qty: 50, uom: "CJ", grStatus: "Completado (411)", putawayStatus: "Confirmado", stockLoc: "ZA01", qrfcQueue: "OK (Verde)" },
        { poNum: "4500012875", poDate: "01.11.2026", vendor: "17300001", vendorName: "AgroExpress Commodities", ibdNum: "180004505", mat: "ZMAT-01", qty: 40, uom: "SC", grStatus: "Completado (411)", putawayStatus: "Confirmado", stockLoc: "ZA01", qrfcQueue: "OK (Verde)" },
        { poNum: "4500012860", poDate: "01.11.2026", vendor: "10300001", vendorName: "Distribuidora Mayorista", ibdNum: "180004490", mat: "ZMAT-03", qty: 30, uom: "BL", grStatus: "Completado (411)", putawayStatus: "Confirmado", stockLoc: "ZA01", qrfcQueue: "OK (Verde)" }
    ]
};
