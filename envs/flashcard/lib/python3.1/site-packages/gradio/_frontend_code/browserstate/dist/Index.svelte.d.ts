import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        storage_key: string;
        secret: string;
        default_value: any;
        value?: any;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {};
};
export type IndexProps = typeof __propDef.props;
export type IndexEvents = typeof __propDef.events;
export type IndexSlots = typeof __propDef.slots;
export default class Index extends SvelteComponent<IndexProps, IndexEvents, IndexSlots> {
    get storage_key(): string;
    /**accessor*/
    set storage_key(_: string);
    get secret(): string;
    /**accessor*/
    set secret(_: string);
    get default_value(): any;
    /**accessor*/
    set default_value(_: any);
    get value(): any;
    /**accessor*/
    set value(_: any);
}
export {};
