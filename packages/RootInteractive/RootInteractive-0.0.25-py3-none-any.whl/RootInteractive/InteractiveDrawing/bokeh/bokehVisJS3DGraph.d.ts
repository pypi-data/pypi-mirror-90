import { LayoutDOM, LayoutDOMView } from "models/layouts/layout_dom";
import { ColumnDataSource } from "models/sources/column_data_source";
import * as p from "core/properties";
declare namespace vis {
    class Graph3d {
        constructor(el: HTMLElement, data: object, OPTIONS: object);
        setData(data: vis.DataSet): void;
        setOptions(options: object): void;
    }
    class DataSet {
        add(data: unknown): void;
    }
}
export declare class BokehVisJSGraph3DView extends LayoutDOMView {
    model: BokehVisJSGraph3D;
    private _graph;
    initialize(): void;
    private _init;
    get_data(): vis.DataSet;
    get child_models(): LayoutDOM[];
    _update_layout(): void;
}
export declare namespace BokehVisJSGraph3D {
    type Attrs = p.AttrsOf<Props>;
    type Props = LayoutDOM.Props & {
        x: p.Property<string>;
        y: p.Property<string>;
        z: p.Property<string>;
        style: p.Property<string>;
        options3D: p.Property<Record<string, any>>;
        data_source: p.Property<ColumnDataSource>;
    };
}
export interface BokehVisJSGraph3D extends BokehVisJSGraph3D.Attrs {
}
export declare class BokehVisJSGraph3D extends LayoutDOM {
    properties: BokehVisJSGraph3D.Props;
    __view_type__: BokehVisJSGraph3DView;
    constructor(attrs?: Partial<BokehVisJSGraph3D.Attrs>);
    static __name__: string;
    static init_BokehVisJSGraph3D(): void;
}
export {};
