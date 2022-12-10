using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using CSP.Models.DB.Chip;
using Syncfusion.Windows.Tools.Controls;

namespace CSP.Modules.Dialogs.NewMCU.Views.Components;

using repository_t =
    Dictionary<string, Dictionary<string, Dictionary<string, Dictionary<string, RepositoryModel.MCUModel>>>>;

public partial class MCUFilterBox
{
    public static readonly DependencyProperty CompanyFilterProperty = DependencyProperty.Register("CompanyFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUFilterBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnCompanyFilterChanged)
            { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty CoreFilterProperty = DependencyProperty.Register("CoreFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUFilterBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnCoreFilterChanged)
            { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty LineFilterProperty = DependencyProperty.Register("LineFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUFilterBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnLineFilterChanged)
            { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty PackageFilterProperty = DependencyProperty.Register("PackageFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUFilterBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnPackageFilterChanged)
            { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty RepositoryProperty = DependencyProperty.Register("Repository",
        typeof(repository_t),
        typeof(MCUFilterBox),
        new FrameworkPropertyMetadata(null, OnRepositoryChanged) { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty SearchTextProperty = DependencyProperty.Register("SearchText",
        typeof(string),
        typeof(MCUFilterBox),
        new FrameworkPropertyMetadata("", OnSearchTextChanged) { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty SeriesFilterProperty = DependencyProperty.Register("SeriesFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUFilterBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnSeriesFilterChanged)
            { BindsTwoWayByDefault = true });

    private readonly Dictionary<string, List<string>> _featureCollection = new(); //Key为过滤器的名称 Value为过滤器的特征
    private readonly List<string>                     _featureFilter     = new();
    private readonly List<string>                     _mcuList           = new();

    public MCUFilterBox() {
        InitializeComponent();
    }

    public ObservableCollection<string> CompanyFilter {
        get => (ObservableCollection<string>)GetValue(CompanyFilterProperty);
        set => SetValue(CompanyFilterProperty, value);
    }

    public ObservableCollection<string> CoreFilter {
        get => (ObservableCollection<string>)GetValue(CoreFilterProperty);
        set => SetValue(CoreFilterProperty, value);
    }

    public ObservableCollection<string> LineFilter {
        get => (ObservableCollection<string>)GetValue(LineFilterProperty);
        set => SetValue(LineFilterProperty, value);
    }

    public ObservableCollection<string> PackageFilter {
        get => (ObservableCollection<string>)GetValue(PackageFilterProperty);
        set => SetValue(PackageFilterProperty, value);
    }

    public repository_t Repository {
        get => (repository_t)GetValue(RepositoryProperty);
        set => SetValue(RepositoryProperty, value);
    }

    public string SearchText {
        get => (string)GetValue(SearchTextProperty);
        set => SetValue(SearchTextProperty, value);
    }

    public ObservableCollection<string> SeriesFilter {
        get => (ObservableCollection<string>)GetValue(SeriesFilterProperty);
        set => SetValue(SeriesFilterProperty, value);
    }

    private static void OnCompanyFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUFilterBox)d).OnCompanyFilterValueChanged(e);
    }

    private static void OnCoreFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUFilterBox)d).OnCoreFilterValueChanged(e);
    }

    private static void OnLineFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUFilterBox)d).OnLineFilterValueChanged(e);
    }

    private static void OnPackageFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUFilterBox)d).OnPackageFilterValueChanged(e);
    }

    private static void OnRepositoryChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUFilterBox)d).OnRepositoryValueChanged(e);
    }

    private static void OnSearchTextChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUFilterBox)d).OnSearchTextValueChanged(e);
    }

    private static void OnSeriesFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUFilterBox)d).OnSeriesFilterValueChanged(e);
    }

    private void AddFeatureCollection(string key, string value) {
        if (_featureCollection[key] == null) {
            return;
        }

        if (!_featureCollection[key].Contains(value)) {
            _featureCollection[key].Add(value);
        }
    }

    private void OnCheckListBoxItemChecked(object sender, ItemCheckedEventArgs e) {
        if (sender is not CheckListBox listBox) {
            return;
        }

        if (e.Item is not CheckListBoxItem item) {
            return;
        }

        if (e.Checked) {
            _featureFilter.Add(item.Content.ToString());
        }
        else {
            _featureFilter.Remove(item.Content.ToString());
        }

        switch (listBox.Tag) {
        case "公司": {
            if (e.Checked) {
                CompanyFilter.Add(item.Content.ToString());
            }
            else {
                CompanyFilter.Remove(item.Content.ToString());
            }

            break;
        }

        case "内核": {
            if (e.Checked) {
                CoreFilter.Add(item.Content.ToString());
            }
            else {
                CoreFilter.Remove(item.Content.ToString());
            }

            break;
        }

        case "系列": {
            if (e.Checked) {
                SeriesFilter.Add(item.Content.ToString());
            }
            else {
                SeriesFilter.Remove(item.Content.ToString());
            }

            break;
        }

        case "产品线": {
            if (e.Checked) {
                LineFilter.Add(item.Content.ToString());
            }
            else {
                LineFilter.Remove(item.Content.ToString());
            }

            break;
        }

        case "封装": {
            if (e.Checked) {
                PackageFilter.Add(item.Content.ToString());
            }
            else {
                PackageFilter.Remove(item.Content.ToString());
            }

            break;
        }
        }

        switch (listBox.Tag) {
        case "公司": {
            UpdateCheckListBoxItemStatus(CheckListBoxCore);
            UpdateCheckListBoxItemStatus(CheckListBoxSeries);
            UpdateCheckListBoxItemStatus(CheckListBoxLine);
            UpdateCheckListBoxItemStatus(CheckListBoxPackage);

            break;
        }

        case "内核": {
            UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
            UpdateCheckListBoxItemStatus(CheckListBoxSeries);
            UpdateCheckListBoxItemStatus(CheckListBoxLine);
            UpdateCheckListBoxItemStatus(CheckListBoxPackage);

            break;
        }

        case "系列": {
            UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
            UpdateCheckListBoxItemStatus(CheckListBoxCore);
            UpdateCheckListBoxItemStatus(CheckListBoxLine);
            UpdateCheckListBoxItemStatus(CheckListBoxPackage);

            break;
        }

        case "产品线": {
            UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
            UpdateCheckListBoxItemStatus(CheckListBoxSeries);
            UpdateCheckListBoxItemStatus(CheckListBoxCore);
            UpdateCheckListBoxItemStatus(CheckListBoxPackage);

            break;
        }

        case "封装": {
            UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
            UpdateCheckListBoxItemStatus(CheckListBoxCore);
            UpdateCheckListBoxItemStatus(CheckListBoxSeries);
            UpdateCheckListBoxItemStatus(CheckListBoxLine);

            break;
        }
        }
    }

    private void OnComboBoxSelectionChanged(object sender, SelectionChangedEventArgs e) {
        if (sender is not ComboBoxAdv comboBox) {
            return;
        }

        SearchText = comboBox.SelectedItem == null ? "" : comboBox.SelectedItem.ToString();

        UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
        UpdateCheckListBoxItemStatus(CheckListBoxCore);
        UpdateCheckListBoxItemStatus(CheckListBoxSeries);
        UpdateCheckListBoxItemStatus(CheckListBoxLine);
        UpdateCheckListBoxItemStatus(CheckListBoxPackage);
    }

    private void OnCompanyFilterValueChanged(DependencyPropertyChangedEventArgs e) {
    }

    private void OnCoreFilterValueChanged(DependencyPropertyChangedEventArgs e) {
    }

    private void OnLineFilterValueChanged(DependencyPropertyChangedEventArgs e) {
    }

    private void OnPackageFilterValueChanged(DependencyPropertyChangedEventArgs e) {
    }

    private void OnRepositoryValueChanged(DependencyPropertyChangedEventArgs e) {
        if (e.NewValue is not repository_t repository) {
            return;
        }

        _featureCollection.Clear();

        ObservableCollection<string> coreList    = new();
        ObservableCollection<string> packageList = new();

        foreach (var (companyName, companies) in repository) {
            if (!_featureCollection.ContainsKey(companyName)) {
                _featureCollection.Add(companyName, new List<string>());
            }

            CheckListBoxCompanies.Items.Add(new CheckListBoxItem {
                Content = companyName
            });

            foreach (var (seriesName, series) in companies) {
                if (!_featureCollection.ContainsKey(seriesName)) {
                    _featureCollection.Add(seriesName, new List<string>());
                }

                CheckListBoxSeries.Items.Add(new CheckListBoxItem {
                    Content = seriesName
                });
                AddFeatureCollection(companyName, seriesName);
                AddFeatureCollection(seriesName, companyName);
                foreach (var (lineName, lines) in series) {
                    if (!_featureCollection.ContainsKey(lineName)) {
                        _featureCollection.Add(lineName, new List<string>());
                    }

                    CheckListBoxLine.Items.Add(new CheckListBoxItem {
                        Content = lineName
                    });
                    AddFeatureCollection(companyName, lineName);
                    AddFeatureCollection(seriesName, lineName);
                    AddFeatureCollection(lineName, companyName);
                    AddFeatureCollection(lineName, seriesName);
                    foreach (var (_, mcu) in lines) {
                        if (!_featureCollection.ContainsKey(mcu.Core)) {
                            _featureCollection.Add(mcu.Core, new List<string>());
                        }

                        if (!_featureCollection.ContainsKey(mcu.Package)) {
                            _featureCollection.Add(mcu.Package, new List<string>());
                        }

                        AddFeatureCollection(companyName, mcu.Core);
                        AddFeatureCollection(companyName, mcu.Package);
                        AddFeatureCollection(companyName, mcu.Name);

                        AddFeatureCollection(seriesName, mcu.Core);
                        AddFeatureCollection(seriesName, mcu.Package);
                        AddFeatureCollection(seriesName, mcu.Name);

                        AddFeatureCollection(lineName, mcu.Core);
                        AddFeatureCollection(lineName, mcu.Package);
                        AddFeatureCollection(lineName, mcu.Name);

                        AddFeatureCollection(mcu.Core, companyName);
                        AddFeatureCollection(mcu.Core, seriesName);
                        AddFeatureCollection(mcu.Core, lineName);
                        AddFeatureCollection(mcu.Core, mcu.Package);
                        AddFeatureCollection(mcu.Core, mcu.Name);

                        AddFeatureCollection(mcu.Package, companyName);
                        AddFeatureCollection(mcu.Package, seriesName);
                        AddFeatureCollection(mcu.Package, lineName);
                        AddFeatureCollection(mcu.Package, mcu.Core);
                        AddFeatureCollection(mcu.Package, mcu.Name);

                        _mcuList.Add(mcu.Name);

                        if (!coreList.Contains(mcu.Core)) {
                            coreList.Add(mcu.Core);
                        }

                        if (!packageList.Contains(mcu.Package)) {
                            packageList.Add(mcu.Package);
                        }
                    }
                }
            }
        }

        ComboBoxMCUName.ItemsSource = _mcuList;

        foreach (string item in coreList) {
            CheckListBoxCore.Items.Add(new CheckListBoxItem {
                Content = item
            });
        }

        foreach (string item in packageList) {
            CheckListBoxPackage.Items.Add(new CheckListBoxItem {
                Content = item
            });
        }
    }

    private void OnSearchTextValueChanged(DependencyPropertyChangedEventArgs e) {
    }

    private void OnSeriesFilterValueChanged(DependencyPropertyChangedEventArgs e) {
    }

    private void UpdateCheckListBoxItemStatus(CheckListBox listBox) {
        foreach (CheckListBoxItem listBoxItem in listBox.Items) {
            if (listBoxItem.Content is string data) {
                if (string.IsNullOrWhiteSpace(SearchText)) {
                    if (_featureFilter.Contains(data) ||
                        _featureCollection[data].Intersect(_featureFilter).Any() ||
                        _featureFilter.Count == 0) {
                        listBoxItem.IsEnabled = true;
                    }
                    else {
                        listBoxItem.IsSelected = false;
                        listBoxItem.IsEnabled  = false;
                    }
                }
                else {
                    if (_featureCollection[data].Contains(SearchText)) {
                        listBoxItem.IsEnabled = true;
                    }
                    else {
                        listBoxItem.IsSelected = false;
                        listBoxItem.IsEnabled  = false;
                    }
                }
            }
        }
    }
}