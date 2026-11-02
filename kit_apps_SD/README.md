# Kit de Apps y Diseño SD / O2C - SAP Build Work Zone
**Proyecto Greenfield Distribuidora Express S.A.**

### Contenido del kit:
- `manifest.json`: Configuración de la UI Integration Card para el ciclo completo Order-to-Cash (O2C).
- `com.avlis.sales.shortcuts.card.zip`: Paquete listo para importar en SAP Build Work Zone.
- `custom-theme-variables.css`: Estilos visuales personalizados para el Launchpad Header y Cards.

### Transacciones y Aplicaciones Incluidas (11 Accesos Clave):
1. **Pedidos de Venta**:
   - `VA01`: Crear Pedido de Ventas (`SalesOrder-create`)
   - `VA02`: Modificar Pedido de Ventas (`SalesOrder-change`)
   - `VA03`: Visualizar Pedido de Ventas (`SalesOrder-display`)
   - `VA05`: Listado / Monitoreo de Pedidos (`SalesOrder-manage`)
2. **Entregas y Expedición**:
   - `VL01N`: Crear Entrega de Salida con Ref. Pedido (`OutboundDelivery-create`)
   - `VL02N`: Modificar Entrega / Picking y Salida de Mercancías (`OutboundDelivery-change`)
   - `VL03N`: Visualizar Entrega de Salida (`OutboundDelivery-display`)
3. **Facturación Comercial**:
   - `VF01`: Crear Documento de Facturación (`BillingDocument-create`)
   - `VF03`: Visualizar Factura Comercial (`BillingDocument-display`)
4. **Gestión Maestra y Almacén**:
   - `BP`: Maestro de Clientes / Business Partner (`BusinessPartner-manage`)
   - `MMBE`: Resumen de Stocks e Inventario por Material (`Material-displayStockOverview`)

### Pasos de Despliegue en SAP Build Work Zone:
1. Ir al **Content Manager** de SAP Build Work Zone.
2. Hacer clic en **Create** / **Import** -> **UI Integration Card**.
3. Seleccionar y cargar `com.avlis.sales.shortcuts.card.zip`.
4. Asignar la tarjeta a un **Catálogo** y a un **Rol** de usuario (ej. Ventas / Facturación).
5. En el **Site Directory**, editar el Sitio/Portal y añadir la tarjeta en la página correspondiente.
6. Aplicar las variables de diseño de `custom-theme-variables.css` si se utiliza un tema personalizado.
