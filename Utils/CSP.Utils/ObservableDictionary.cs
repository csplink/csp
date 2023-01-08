// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
//
// @author      xqyjlj
// @file        ObservableDictionary.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Linq;

namespace CSP.Utils;

public class ObservableDictionary<TKey, TValue> : Dictionary<TKey, TValue>, INotifyCollectionChanged,
    INotifyPropertyChanged
{
    private int _index;

    public new int Count => base.Count;

    public new KeyCollection Keys => base.Keys;

    public new ValueCollection Values => base.Values;

    public new TValue this[TKey key] {
        get => GetValue(key);
        set => SetValue(key, value);
    }

    public TValue this[int index] {
        get => GetIndexValue(index);
        set => SetIndexValue(index, value);
    }

    public event NotifyCollectionChangedEventHandler CollectionChanged;

    public event PropertyChangedEventHandler PropertyChanged;

    public new void Add(TKey key, TValue value) {
        base.Add(key, value);
        OnCollectionChanged(
            new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Add, FindPair(key), _index));
        OnPropertyChanged("Keys");
        OnPropertyChanged("Values");
        OnPropertyChanged("Count");
    }

    public void Add(KeyValuePair<TKey, TValue> keyValuePair) {
        Add(keyValuePair.Key, keyValuePair.Value);
    }

    public new void Clear() {
        base.Clear();
        OnCollectionChanged(new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Reset));
        OnPropertyChanged("Keys");
        OnPropertyChanged("Values");
        OnPropertyChanged("Count");
    }

    public new bool Remove(TKey key) {
        KeyValuePair<TKey, TValue> pair = FindPair(key);
        if (base.Remove(key)) {
            OnCollectionChanged(
                new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Remove, pair, _index));
            OnPropertyChanged("Keys");
            OnPropertyChanged("Values");
            OnPropertyChanged("Count");

            return true;
        }

        return false;
    }

    protected void OnCollectionChanged(NotifyCollectionChangedEventArgs e) {
        CollectionChanged?.Invoke(this, e);
    }

    protected void OnPropertyChanged(string propertyName) {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    #region private方法

    private KeyValuePair<TKey, TValue> FindPair(TKey key) {
        _index = 0;
        foreach (KeyValuePair<TKey, TValue> item in this) {
            if (item.Key.Equals(key)) {
                return item;
            }

            _index++;
        }

        return default;
    }

    private TValue GetIndexValue(int index) {
        for (int i = 0; i < Count; i++) {
            if (i == index) {
                KeyValuePair<TKey, TValue> pair = this.ElementAt(i);

                return pair.Value;
            }
        }

        return default;
    }

    private TValue GetValue(TKey key) {
        return ContainsKey(key) ? base[key] : default;
    }

    private int IndexOf(TKey key) {
        int index = 0;
        foreach (KeyValuePair<TKey, TValue> item in this) {
            if (item.Key.Equals(key)) {
                return index;
            }

            index++;
        }

        return -1;
    }

    private void SetIndexValue(int index, TValue value) {
        try {
            KeyValuePair<TKey, TValue> pair = this.ElementAtOrDefault(index);
            SetValue(pair.Key, value);
        }
        catch (Exception) {
            // ignored
        }
    }

    private void SetValue(TKey key, TValue value) {
        if (ContainsKey(key)) {
            KeyValuePair<TKey, TValue> pair  = FindPair(key);
            int                        index = _index;
            base[key] = value;
            KeyValuePair<TKey, TValue> newPair = FindPair(key);
            OnCollectionChanged(new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Replace, newPair,
                pair, index));
            OnPropertyChanged("Values");
            OnPropertyChanged("Item[]");
        }
        else {
            Add(key, value);
        }
    }

    #endregion private方法
}