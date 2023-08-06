#data loading and bunching; defines the dataloader and items
#contains the basic item Sequence, the basic itemlist SeqList, 

from fastai import *
from fastai.text import *
from iterators import *
from transform import *

supported_seqfiletypes = ['.fastq', '.fna', '.fasta', '.ffn', '.faa']

seqfiletype_to_iterator = {
    '.fastq': FastqIterator,
    '.fna': FastaIterator,
    '.fasta': FastaIterator,
    '.ffn': FastaIterator,
    '.faa': FastaIterator
}

def _get_bio_files(parent, p, f, extensions):
    p = Path(p)#.relative_to(parent)
    if isinstance(extensions,str): extensions = [extensions]
    low_extensions = [e.lower() for e in extensions] if extensions is not None else None
    res = [p/o for o in f if not o.startswith('.')
           and (extensions is None or f'.{o.split(".")[-1].lower()}' in low_extensions)]
    return res

def get_bio_files(path:PathOrStr, extensions:Collection[str]=None, recurse:bool=True, exclude:Optional[Collection[str]]=None,
              include:Optional[Collection[str]]=None, presort:bool=False, followlinks:bool=False)->FilePathList:
    "Return list of files in `path` that have a suffix in `extensions`; optionally `recurse`."
    low_extensions = [e.lower() for e in extensions] if extensions is not None else None
    if recurse:
        res = []
        for i,(p,d,f) in enumerate(os.walk(path, followlinks=followlinks)):
            # skip hidden dirs
            if include is not None and i==0:   d[:] = [o for o in d if o in include]
            elif exclude is not None and i==0: d[:] = [o for o in d if o not in exclude]
            else:                              d[:] = [o for o in d if not o.startswith('.')]
            res += _get_bio_files(path, p, f, extensions)
        if presort: res = sorted(res, key=lambda p: _path_to_same_str(p), reverse=False)
        return res
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        res = _get_bio_files(path, path, f, extensions)
        if presort: res = sorted(res, key=lambda p: _path_to_same_str(p), reverse=False)
        return res

def check_seqfiletype(filename:PathOrStr, extensions:Collection[str]=supported_seqfiletypes):
    if isinstance(filename, Path): 
        seqfiletype = filename.suffix
    else:
        seqfiletype = f'.{filename.split(".")[-1].lower()}' 
    assert seqfiletype in extensions, "Input sequence file type %r is not supported." % seqfiletype
    return seqfiletype

def get_items_from_seqfile(filename:PathOrStr, extensions:Collection[str]=supported_seqfiletypes, max_seqs:int=None, skiprows:int=0, ksize:int=None):
    seqfiletype = check_seqfiletype(filename, extensions)
    iterator = seqfiletype_to_iterator[seqfiletype]
    with open(filename, "r") as handle:
        items = []
        row = 0 
        for title, seq, qual, offset in iterator(handle):
            #get (filename, offset, length of sequence) for each read and add to items
            row += 1
            if len(seq)>=ksize and row>skiprows:
                items.append(seq)
            if max_seqs and (row-skiprows)>=max_seqs: 
                break
    handle.close()
    return items

def get_count_from_seqfile(filename:PathOrStr, extensions:Collection[str]=supported_seqfiletypes, max_seqs:int=None):
    seqfiletype = check_seqfiletype(filename, extensions)
    iterator = seqfiletype_to_iterator[seqfiletype]
    with open(filename, "r") as handle:
        count = 0
        for title, seq, qual, offset in iterator(handle):
            count += 1
            if max_seqs and count >= max_seqs: 
                break
    handle.close()
    return count

def extract_from_header(filename:PathOrStr, func:Callable, extensions:Collection[str]=supported_seqfiletypes, max_seqs:int=None):
    seqfiletype = check_seqfiletype(filename, extensions)
    iterator = seqfiletype_to_iterator[seqfiletype]
    with open(filename, "r") as handle:
        extracts = []
        row = 0
        for title, seq, qual, offset in iterator(handle):
            extract = func(title)
            extracts.append(extract)
            row += 1
            if max_seqs and row >= max_seqs: 
                break
    handle.close()
    return extracts

def get_df_from_files(files, max_seqs_per_file, skiprows, header, delimiter):
    df = pd.DataFrame()
    for csv_name in files:
            chunk = pd.read_csv(csv_name, nrows=max_seqs_per_file, skiprows=range(1,skiprows+1), header=header, delimiter=delimiter)
            df = df.append(chunk)
    return df

class OpenSeqFileProcessor(PreProcessor):
    "`PreProcessor` that opens the filenames and read the sequences. This is used if creating biotextlists from_folder, because need to know the path of each input for splitting."
    def __init__(self, ds:ItemList=None, extensions:Collection[str]=supported_seqfiletypes, max_seqs:int=None, skiprows:int=0, ksize:int=None):
        self.extensions = extensions
        self.max_seqs = max_seqs
        self.ksize = ksize
        self.skiprows=skiprows

    def process(self, ds:Collection): 
        readitems = []
        for item in ds.items:
            readitems.extend(self.process_one(item))
        ds.items = readitems

    def process_one(self,item): 
        return get_items_from_seqfile(item, extensions=self.extensions, max_seqs=self.max_seqs, skiprows=self.skiprows, ksize=self.ksize) if isinstance(item, Path) else [item]

class BioTextList(TextList):
    def __init__(self, items:Iterator, vocab:BioVocab=None, pad_idx:int=1, sep=' ', **kwargs):
        super().__init__(items, **kwargs)

    def label_for_lm(self, **kwargs):
        "A special labelling method for language models."
        self.__class__ = BioLMTextList
        kwargs['label_cls'] = LMLabelList
        return self.label_const(0, **kwargs)

    def label_for_df_for_regression(self, cols:IntsOrStrs=1, label_cls:Callable=FloatList, **kwargs):
        "Label `self.items` from the values in `cols` in `self.inner_df`."
        labels = self.inner_df.iloc[:,df_names_to_idx(cols, self.inner_df)]
        assert labels.isna().sum().sum() == 0, f"You have NaN values in column(s) {cols} of your dataframe, please fix it."
        return self._label_from_list(labels, label_cls=label_cls, **kwargs)
   
       
    @classmethod
    def from_seqfile(cls, filename:PathOrStr, path:PathOrStr='.', extensions:Collection[str]=supported_seqfiletypes, max_seqs_per_file:int=None, skiprows:int=0, ksize:int=None, **kwargs)->'TextList':
        "Creates a SeqList from a single sequence file (e.g. .fastq, .fasta, etc.)"
        #get (filename, offset) tuple for each read and add to items
        items = get_items_from_seqfile(filename=filename, extensions=extensions, max_seqs=max_seqs_per_file, skiprows=skiprows, ksize=ksize)
        
        return cls(items=items, path=path, **kwargs)

    @classmethod
    def from_folder(cls, path:PathOrStr='.', vocab:Vocab=None, extensions:Collection[str]=supported_seqfiletypes, 
                        max_seqs_per_file:int=None, skiprows:int=0, recurse:bool=True, processor:PreProcessor=None, **kwargs) -> 'TextList':
        "Creates a SeqList from all sequence files in a folder"
        #get list of files in `path` with seqfile suffixes. `recurse` determines if we search subfolders.
        files = get_bio_files(path=path, extensions=extensions, recurse=recurse)
        #define processor with OpenSeqFileProcessor since items are now a list of filepaths rather than Seq objects
        processor = ifnone(processor, [OpenSeqFileProcessor(max_seqs=max_seqs_per_file, skiprows=skiprows), BioTokenizeProcessor(), BioNumericalizeProcessor(vocab=vocab)])

        return cls(items=files, path=path, processor=processor, **kwargs)

    def label_from_fname(self, label_cls:Callable=None, max_seqs_per_file:int=None, extensions:Collection[str]=supported_seqfiletypes, **kwargs) -> 'LabelList':
        #give label to each filename depending on the filename
        labels = []
        for o in self.items:
            #extract label from filename
            label = ".".join((o.parts if isinstance(o, Path) else o.split(os.path.sep))[-1].split(".")[0:-1])
            #number of times should repeat that label
            count = get_count_from_seqfile(filename=o, extensions=extensions, max_seqs=max_seqs_per_file)
            labels.extend([label]*count)
        classes = list(set(labels))
        #kwargs = {dict(classes=classes),**kwargs}

        return self._label_from_list([labels],label_cls=label_cls, classes=classes, **kwargs)

    def label_from_header(self, func:Callable, label_cls:Callable=None, max_seqs_per_file:int=None, extensions:Collection[str]=supported_seqfiletypes, **kwargs) -> 'LabelList':
        #items need to be a list of filenames, as imported from from_folder (not from_seqfile) 
        labels = []
        for o in self.items:
            #extract label from filename
            extracts = extract_from_header(filename=o, func=func, extensions=extensions, max_seqs=max_seqs_per_file)
            labels.extend(extracts)

        return self._label_from_list(labels,label_cls=label_cls, **kwargs)

class BioItemLists(ItemLists):

    def __getattr__(self, k):
        ft = getattr(self.train, k)
        if not isinstance(ft, Callable): return ft
        fv = getattr(self.valid, k)
        assert isinstance(fv, Callable)
        def _inner(*args, **kwargs):
            self.train = ft(*args, from_item_lists=True, **kwargs)
            assert isinstance(self.train, LabelList)
            kwargs['label_cls'] = self.train.y.__class__
            self.valid = fv(*args, from_item_lists=True, **kwargs)
            self.__class__ = BioLabelLists
            self.process()
            return self
        return _inner

class BioLabelLists(LabelLists):
    "A `LabelList` for each of `train` and `valid` (optional `test`)."
    def get_processors(self):
        "Read the default class processors if none have been set."
        default_xp = get_lol_processor()
        default_yp = []
        #enable separate processors for train and valid set (intended for reading different numbers of sequences from files in train and valid sets)
        xp = ifnone(self.train.x.processor, default_xp)
        yp = ifnone(self.train.y.processor, default_yp)
        v_xp = ifnone(self.valid.x.processor, default_xp)
        v_yp = ifnone(self.valid.y.processor, default_yp)
        return xp,yp,v_xp,v_yp

    def process(self):
        "Process the inner datasets."
        xp,yp,v_xp,v_yp = self.get_processors()
        #process train
        self.lists[0].process(xp,yp,name='train')
        #process valid
        self.lists[1].process(v_xp,v_yp,name='valid')
        #process test if it exists with the same processor as valid
        if len(self.lists)>2:
            self.lists[2].process(v_xp,v_yp,name='test')
        #progress_bar clear the outputs so in some case warnings issued during processing disappear.
        for ds in self.lists:
            if getattr(ds, 'warn', False): warn(ds.warn)
        return self

class BioDataBunch(TextDataBunch):
    @classmethod
    def from_folder(cls, path:PathOrStr, train:str='train', valid:str='valid', test:Optional[str]=None, valid_pct:float=0.2,
                    extensions:Collection[str]=supported_seqfiletypes, recurse:bool=True, ksize:int=None,
                    max_seqs_per_file:int=None, val_maxseqs:int=None, skiprows:int=0, val_skiprows:int=0,
                    classes:Collection[Any]=None, tokenizer:Tokenizer=None, vocab:Vocab=None, chunksize:int=10000, max_vocab:int=60000,
                    min_freq:int=2, mark_fields:bool=False, include_bos:bool=True, include_eos:bool=False, seed:int=None, **kwargs):
        "Create a `BioDataBunch` from fasta/sequence files in folders."
        path = Path(path).absolute()

        if train and valid:
            processor = [OpenSeqFileProcessor(extensions=extensions, max_seqs=max_seqs_per_file, ksize=ksize, skiprows=skiprows)] + get_lol_processor(tokenizer=tokenizer, vocab=vocab, chunksize=chunksize, max_vocab=max_vocab,
                                   min_freq=min_freq, include_bos=include_bos, include_eos=include_eos)
            v_processor = [OpenSeqFileProcessor(extensions=extensions, max_seqs=val_maxseqs, ksize=ksize, skiprows=val_skiprows)] + get_lol_processor(tokenizer=tokenizer, vocab=vocab, chunksize=chunksize, max_vocab=max_vocab,
                                   min_freq=min_freq, include_bos=include_bos, include_eos=include_eos)
            
            src = BioItemLists(path, BioTextList.from_folder(path=Path(path)/Path(train), vocab=vocab, extensions=extensions, max_seqs_per_file=max_seqs_per_file, skiprows=skiprows, recurse=recurse, processor=processor),
                        BioTextList.from_folder(path=Path(path)/Path(valid), vocab=vocab, extensions=extensions, max_seqs_per_file=val_maxseqs, skiprows=val_skiprows, recurse=recurse, processor=v_processor))

        else:
            processor = [OpenSeqFileProcessor(extensions=extensions, max_seqs=max_seqs_per_file, ksize=ksize)] + get_lol_processor(tokenizer=tokenizer, vocab=vocab, chunksize=chunksize, max_vocab=max_vocab,
                                   min_freq=min_freq, include_bos=include_bos, include_eos=include_eos)
            src = BioTextList.from_folder(path=path, vocab=vocab, extensions=extensions, max_seqs_per_file=max_seqs_per_file, recurse=recurse, processor=processor)                                   
            src = src.split_by_rand_pct(valid_pct=valid_pct, seed=seed)

        src = src.label_for_lm() if cls==BioLMDataBunch else src.label_from_folder(classes=classes)
        if test is not None: src.add_test_folder(path/test)
        return src.databunch(**kwargs)

    @classmethod
    def from_seqfile(cls, path:PathOrStr, filename:PathOrStr, test_filename:PathOrStr, extensions:Collection[str]=supported_seqfiletypes,
                    max_seqs_per_file:int=None,skiprows:int=0,valid_pct:float=0.2, seed:int=None, 
                    vocab:BioVocab=None, tokenizer:BioTokenizer=None,
                    chunksize:int=10000, max_vocab:int=60000, min_freq:int=2, include_bos:bool=None, include_eos:bool=None,
                    label_func:Callable=None, **kwargs:Any):
        #Create from sequence file. Not recommended for classifiers - you need to provide a fairly complicated labeling function
        processor = get_lol_processor(tokenizer=tokenizer, vocab=vocab, chunksize=chunksize, max_vocab=max_vocab,
                                   min_freq=min_freq, include_bos=include_bos, include_eos=include_eos)
        
        src = BioTextList.from_seqfile(filename=filename, path=path, extensions=extensions, max_seqs_per_file=max_seqs_per_file, skiprows=skiprows, processor=processor)
        src = src.split_by_rand_pct(valid_pct=valid_pct, seed=seed)
        src = src.label_for_lm() if cls==BioLMDataBunch else src.label_from_func(label_func, **kwargs)

        if test is not None: src.add_test(BioTextList.from_seqfile(test_filename, path))

        return src.databunch(**kwargs)

    @classmethod
    def from_df(cls, path:PathOrStr, train_df:DataFrame, valid_df:DataFrame, test_df:Optional[DataFrame]=None,
                tokenizer:Tokenizer=None, vocab:Vocab=None, classes:Collection[str]=None, 
                text_cols:IntsOrStrs=1,label_cols:IntsOrStrs=0, 
                label_delim:str=None, chunksize:int=10000, max_vocab:int=60000,
                min_freq:int=2, mark_fields:bool=False, include_bos:bool=True, include_eos:bool=False,
                seed:int=None, **kwargs) -> DataBunch:

        path = Path(path).absolute()
        processor = get_lol_processor(tokenizer=tokenizer, vocab=vocab, chunksize=chunksize, max_vocab=max_vocab,
                                   min_freq=min_freq, include_bos=include_bos, include_eos=include_eos)
        
        if classes is None and is_listy(label_cols) and len(label_cols) > 1: classes = label_cols
        src = ItemLists(path, TextList.from_df(train_df, path, cols=text_cols, processor=processor),
                        TextList.from_df(valid_df, path, cols=text_cols, processor=processor))
        if cls==TextLMDataBunch: src = src.label_for_lm()
        else: 
            if label_delim is not None: src = src.label_from_df(cols=label_cols, classes=classes, label_delim=label_delim)
            else: src = src.label_from_df(cols=label_cols, classes=classes)
        if test_df is not None: src.add_test(TextList.from_df(test_df, path, cols=text_cols))

        return src.databunch(**kwargs)

    @classmethod
    def from_multiple_csv(cls, path:PathOrStr, extensions:Collection[str]=['.csv'], recurse:bool=False, 
                    max_seqs_per_file:int=None, valid_max_seqs:int=None, skiprows:int=0,
                    delimiter:str=None, header='infer', text_cols:IntsOrStrs=1, label_cols:IntsOrStrs=0, label_delim:str=None,
                    valid_pct:float=0.2, train:str=None, valid:str=None, test:Optional[str]=None,
                    classes:Collection[str]=None, 
                    tokenizer:BioTokenizer=None, vocab:BioVocab=None, 
                    chunksize:int=10000, max_vocab:int=60000, min_freq:int=2, include_bos:bool=None, include_eos:bool=None, 
                    seed:int=None, **kwargs) -> DataBunch:

        path = Path(path).absolute()

        processor = get_lol_processor(tokenizer=tokenizer, vocab=vocab, chunksize=chunksize, max_vocab=max_vocab,
                                   min_freq=min_freq, include_bos=include_bos, include_eos=include_eos)

        if train and valid:
            train_files, valid_files = get_bio_files(path=Path(path)/Path(train).resolve(), extensions=extensions, recurse=recurse), get_bio_files(path=Path(path)/Path(valid).resolve(), extensions=extensions, recurse=recurse)
            test_files = (None if test is None else get_bio_files(path=Path(path)/Path(test).resolve(), extensions=extensions, recurse=recurse))
            train_df = get_df_from_files(train_files, max_seqs_per_file=max_seqs_per_file, skiprows=skiprows, header=header, delimiter=delimiter)
            valid_df = get_df_from_files(valid_files, max_seqs_per_file=valid_max_seqs, skiprows=0, header=header, delimiter=delimiter)
            test_df = (None if test_files is None else get_df_from_files(test_files, max_seqs_per_file=max_seqs_per_file, skiprows=skiprows, header=header, delimiter=delimiter))
        else:
            #get a list of csv files in path
            files = get_bio_files(path=path, extensions=extensions, recurse=recurse)
            #for each file, read the csv (optionally with max_seqs and skiprows) and append to the total df
            train_df, valid_df, test_df = (pd.DataFrame(), pd.DataFrame(), (None if test is None else pd.DataFrame()))
            for csv_name in files:
                df = pd.read_csv(csv_name, nrows=max_seqs_per_file, skiprows=range(1,skiprows+1), header=header, delimiter=delimiter)
                df = df.iloc[np.random.RandomState(seed=seed).permutation(len(df))] #if seed is None, this will make the validation set diff between passes if do multiple pass-throughs of the data for big chunks; should set seed, or make sure you don't do multiple passthroughs
                cut = int(valid_pct * len(df)) + 1
                train_chunk, valid_chunk = df[cut:], df[:cut]
                if test is not None:
                    test_chunk = pd.read_csv(Path(path)/test, header=header, delimiter=delimiter)
                    test_df = test_df.append(test_chunk)
                train_df = train_df.append(train_chunk)
                valid_df = valid_df.append(valid_chunk)
        train_df.reset_index(drop=True, inplace=True)
        valid_df.reset_index(drop=True, inplace=True)
        
        if test_df is not None:
            test_df.reset_index(drop=True, inplace=True)

        if classes is None and is_listy(label_cols) and len(label_cols) > 1: classes = label_cols
        src = ItemLists(path, BioTextList.from_df(train_df, path, cols=text_cols, processor=processor),
                        BioTextList.from_df(valid_df, path, cols=text_cols, processor=processor))
        if cls==TextLMDataBunch: src = src.label_for_lm()
        else: 
            if label_delim is not None: src = src.label_from_df(cols=label_cols, classes=classes, label_delim=label_delim)
            else: src = src.label_from_df(cols=label_cols, classes=classes)
        if test_df is not None: src.add_test(BioTextList.from_df(test_df, path, cols=text_cols))

        return src.databunch(**kwargs)
    
class BioLMDataBunch(BioDataBunch):
    "Create a `BioDataBunch` suitable for training a language model. This is the same as TextLMDataBunch but inherits from BioDataBunch."
    @classmethod
    def create(cls, train_ds, valid_ds, test_ds=None, path:PathOrStr='.', no_check:bool=False, bs:int=64, val_bs:int=None,
               num_workers:int=0, device:torch.device=None, collate_fn:Callable=data_collate,
               dl_tfms:Optional[Collection[Callable]]=None, bptt:int=70, backwards:bool=False, **dl_kwargs) -> DataBunch:
        "Create a `BioDataBunch` in `path` from the `datasets` for language modelling. Passes `**dl_kwargs` on to `DataLoader()`"
        datasets = cls._init_ds(train_ds, valid_ds, test_ds)
        val_bs = ifnone(val_bs, bs)
        datasets = [LanguageModelPreLoader(ds, shuffle=(i==0), bs=(bs if i==0 else val_bs), bptt=bptt, backwards=backwards)
                    for i,ds in enumerate(datasets)]
        val_bs = bs
        dls = [DataLoader(d, b, shuffle=False, **dl_kwargs) for d,b in zip(datasets, (bs,val_bs,val_bs,val_bs)) if d is not None]
        return cls(*dls, path=path, device=device, dl_tfms=dl_tfms, collate_fn=collate_fn, no_check=no_check)

class BioClasDataBunch(BioDataBunch):
    "Create a `BioDataBunch` suitable for training an RNN classifier. This is the same as TextClasDataBunch but inherits from BioDataBunch."
    @classmethod
    def create(cls, train_ds, valid_ds, test_ds=None, path:PathOrStr='.', bs:int=32, val_bs:int=None, pad_idx=1,
               pad_first=True, device:torch.device=None, no_check:bool=False, backwards:bool=False, 
               dl_tfms:Optional[Collection[Callable]]=None, **dl_kwargs) -> DataBunch:
        "Function that transform the `datasets` in a `DataBunch` for classification. Passes `**dl_kwargs` on to `DataLoader()`"
        datasets = cls._init_ds(train_ds, valid_ds, test_ds)
        val_bs = ifnone(val_bs, bs)
        collate_fn = partial(pad_collate, pad_idx=pad_idx, pad_first=pad_first, backwards=backwards)
        train_sampler = SortishSampler(datasets[0].x, key=lambda t: len(datasets[0][t][0].data), bs=bs)
        train_dl = DataLoader(datasets[0], batch_size=bs, sampler=train_sampler, drop_last=True, **dl_kwargs)
        dataloaders = [train_dl]
        for ds in datasets[1:]:
            lengths = [len(t) for t in ds.x.items]
            sampler = SortSampler(ds.x, key=lengths.__getitem__)
            dataloaders.append(DataLoader(ds, batch_size=val_bs, sampler=sampler, **dl_kwargs))
        return cls(*dataloaders, path=path, device=device, dl_tfms=dl_tfms, collate_fn=collate_fn, no_check=no_check)

class BioLMTextList(BioTextList):
    "Special `BioTextList` for a language model."
    _bunch = BioLMDataBunch
    _is_lm = True