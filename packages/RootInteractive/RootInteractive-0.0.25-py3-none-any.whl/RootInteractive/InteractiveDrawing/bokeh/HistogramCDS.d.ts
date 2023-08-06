import { ColumnarDataSource } from "models/sources/columnar_data_source";
import { ColumnDataSource } from "models/sources/column_data_source";
import * as p from "core/properties";
export declare namespace HistogramCDS {
    type Attrs = p.AttrsOf<Props>;
    type Props = ColumnarDataSource.Props & {
        source: p.Property<ColumnDataSource>;
        nbins: p.Property<number>;
        range_min: p.Property<number>;
        range_max: p.Property<number>;
        sample: p.Property<string>;
        weights: p.Property<string | null>;
    };
}
export interface HistogramCDS extends HistogramCDS.Attrs {
}
export declare class HistogramCDS extends ColumnarDataSource {
    properties: HistogramCDS.Props;
    constructor(attrs?: Partial<HistogramCDS.Attrs>);
    static __name__: string;
    static init_HistogramCDS(): void;
    initialize(): void;
    connect_signals(): void;
    update_data(indices?: number[] | null): void;
    private _transform_origin;
    private _transform_scale;
    private _range_min;
    private _range_max;
    private _nbins;
    view: number[] | null;
    update_range(): void;
    getbin(val: number): number;
}
