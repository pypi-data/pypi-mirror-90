import { ColumnarDataSource } from "models/sources/columnar_data_source";
import { ColumnDataSource } from "models/sources/column_data_source";
import * as p from "core/properties";
export declare namespace Histo2dCDS {
    type Attrs = p.AttrsOf<Props>;
    type Props = ColumnarDataSource.Props & {
        source: p.Property<ColumnDataSource>;
        nbins: p.Property<number[]>;
        range: p.Property<(number[] | null)[] | null>;
        sample_x: p.Property<string>;
        sample_y: p.Property<string>;
        weights: p.Property<string | null>;
    };
}
export interface Histo2dCDS extends Histo2dCDS.Attrs {
}
export declare class Histo2dCDS extends ColumnarDataSource {
    properties: Histo2dCDS.Props;
    constructor(attrs?: Partial<Histo2dCDS.Attrs>);
    static __name__: string;
    static init_Histo2dCDS(): void;
    initialize(): void;
    connect_signals(): void;
    update_data(indices?: number[] | null): void;
    private _transform_origin_x;
    private _transform_origin_y;
    private _transform_scale_x;
    private _transform_scale_y;
    private _stride;
    private _range_min;
    private _range_max;
    private _nbins;
    view: number[] | null;
    private _bin_indices;
    update_range(): void;
    getbin(idx: number, x_arr: number[], y_arr: number[]): number;
}
