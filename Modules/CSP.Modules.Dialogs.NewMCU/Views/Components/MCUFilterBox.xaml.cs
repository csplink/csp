using CSP.Utils.Extensions;
using Syncfusion.Windows.Tools.Controls;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using CSP.Modules.Dialogs.NewMCU.Models;

namespace CSP.Modules.Dialogs.NewMCU.Views.Components
{
    public partial class MCUFilterBox
    {
        public static readonly DependencyProperty CompanyFilterProperty = DependencyProperty.Register("CompanyFilter",
            typeof(ObservableCollection<string>),
            typeof(MCUFilterBox),
            new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnCompanyFilterChanged) { BindsTwoWayByDefault = true });

        public static readonly DependencyProperty CoreFilterProperty = DependencyProperty.Register("CoreFilter",
            typeof(ObservableCollection<string>),
            typeof(MCUFilterBox),
            new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnCoreFilterChanged) { BindsTwoWayByDefault = true });

        public static readonly DependencyProperty LineFilterProperty = DependencyProperty.Register("LineFilter",
            typeof(ObservableCollection<string>),
            typeof(MCUFilterBox),
            new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnLineFilterChanged) { BindsTwoWayByDefault = true });

        public static readonly DependencyProperty PackageFilterProperty = DependencyProperty.Register("PackageFilter",
            typeof(ObservableCollection<string>),
            typeof(MCUFilterBox),
            new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnPackageFilterChanged) { BindsTwoWayByDefault = true });

        public static readonly DependencyProperty RepositoryProperty = DependencyProperty.Register("Repository",
            typeof(RepositoryModel),
            typeof(MCUFilterBox),
            new FrameworkPropertyMetadata(null, OnRepositoryChanged) { BindsTwoWayByDefault = true });

        public static readonly DependencyProperty SearchTextProperty = DependencyProperty.Register("SearchText",
            typeof(string),
            typeof(MCUFilterBox),
            new FrameworkPropertyMetadata("", OnSearchTextChanged) { BindsTwoWayByDefault = true });

        public static readonly DependencyProperty SeriesFilterProperty = DependencyProperty.Register("SeriesFilter",
            typeof(ObservableCollection<string>),
            typeof(MCUFilterBox),
            new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnSeriesFilterChanged) { BindsTwoWayByDefault = true });

        private readonly Dictionary<string, List<string>> _featureCollection = new(); //Key为过滤器的名称 Value为过滤器的特征
        private readonly List<string> _featureFilter = new();
        private readonly List<string> _mcuList = new();

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

        public RepositoryModel Repository {
            get => (RepositoryModel)GetValue(RepositoryProperty);
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
            if (_featureCollection[key] == null)
                return;

            if (!_featureCollection[key].Contains(value)) {
                _featureCollection[key].Add(value);
            }
        }

        private void OnCheckListBoxItemChecked(object sender, ItemCheckedEventArgs e) {
            if (sender is not CheckListBox listBox)
                return;

            if (e.Item is not CheckListBoxItem item)
                return;

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
                    }
                    break;

                case "内核": {
                        if (e.Checked) {
                            CoreFilter.Add(item.Content.ToString());
                        }
                        else {
                            CoreFilter.Remove(item.Content.ToString());
                        }
                    }
                    break;

                case "系列": {
                        if (e.Checked) {
                            SeriesFilter.Add(item.Content.ToString());
                        }
                        else {
                            SeriesFilter.Remove(item.Content.ToString());
                        }
                    }
                    break;

                case "产品线": {
                        if (e.Checked) {
                            LineFilter.Add(item.Content.ToString());
                        }
                        else {
                            LineFilter.Remove(item.Content.ToString());
                        }
                    }
                    break;

                case "封装": {
                        if (e.Checked) {
                            PackageFilter.Add(item.Content.ToString());
                        }
                        else {
                            PackageFilter.Remove(item.Content.ToString());
                        }
                    }
                    break;
            }

            switch (listBox.Tag) {
                case "公司": {
                        UpdateCheckListBoxItemStatus(CheckListBoxCore);
                        UpdateCheckListBoxItemStatus(CheckListBoxSeries);
                        UpdateCheckListBoxItemStatus(CheckListBoxLine);
                        UpdateCheckListBoxItemStatus(CheckListBoxPackage);
                    }
                    break;

                case "内核": {
                        UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
                        UpdateCheckListBoxItemStatus(CheckListBoxSeries);
                        UpdateCheckListBoxItemStatus(CheckListBoxLine);
                        UpdateCheckListBoxItemStatus(CheckListBoxPackage);
                    }
                    break;

                case "系列": {
                        UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
                        UpdateCheckListBoxItemStatus(CheckListBoxCore);
                        UpdateCheckListBoxItemStatus(CheckListBoxLine);
                        UpdateCheckListBoxItemStatus(CheckListBoxPackage);
                    }
                    break;

                case "产品线": {
                        UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
                        UpdateCheckListBoxItemStatus(CheckListBoxSeries);
                        UpdateCheckListBoxItemStatus(CheckListBoxCore);
                        UpdateCheckListBoxItemStatus(CheckListBoxPackage);
                    }
                    break;

                case "封装": {
                        UpdateCheckListBoxItemStatus(CheckListBoxCompanies);
                        UpdateCheckListBoxItemStatus(CheckListBoxCore);
                        UpdateCheckListBoxItemStatus(CheckListBoxSeries);
                        UpdateCheckListBoxItemStatus(CheckListBoxLine);
                    }
                    break;
            }
        }

        private void OnComboBoxSelectionChanged(object sender, SelectionChangedEventArgs e) {
            if (sender is not ComboBoxAdv comboBox)
                return;

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
            if (e.NewValue is not RepositoryModel value)
                return;

            _featureCollection.Clear();

            var coreList = new ObservableCollection<string>();
            var packageList = new ObservableCollection<string>();

            foreach (var company in value.Companies) {
                if (!_featureCollection.ContainsKey(company.Name))
                    _featureCollection.Add(company.Name, new List<string>());

                CheckListBoxCompanies.Items.Add(new CheckListBoxItem {
                    Content = company.Name
                });

                foreach (var series in company.Series) {
                    if (!_featureCollection.ContainsKey(series.Name))
                        _featureCollection.Add(series.Name, new List<string>());

                    CheckListBoxSeries.Items.Add(new CheckListBoxItem {
                        Content = series.Name
                    });
                    AddFeatureCollection(company.Name, series.Name);
                    AddFeatureCollection(series.Name, company.Name);

                    foreach (var line in series.Lines) {
                        if (!_featureCollection.ContainsKey(line.Name))
                            _featureCollection.Add(line.Name, new List<string>());

                        CheckListBoxLine.Items.Add(new CheckListBoxItem {
                            Content = line.Name
                        });

                        AddFeatureCollection(company.Name, line.Name);
                        AddFeatureCollection(series.Name, line.Name);
                        AddFeatureCollection(line.Name, company.Name);
                        AddFeatureCollection(line.Name, series.Name);

                        foreach (var mcu in line.MCU) {
                            if (!_featureCollection.ContainsKey(mcu.Core))
                                _featureCollection.Add(mcu.Core, new List<string>());

                            if (!_featureCollection.ContainsKey(mcu.Package))
                                _featureCollection.Add(mcu.Package, new List<string>());

                            AddFeatureCollection(company.Name, mcu.Core);
                            AddFeatureCollection(company.Name, mcu.Package);
                            AddFeatureCollection(company.Name, mcu.Name);

                            AddFeatureCollection(series.Name, mcu.Core);
                            AddFeatureCollection(series.Name, mcu.Package);
                            AddFeatureCollection(series.Name, mcu.Name);

                            AddFeatureCollection(line.Name, mcu.Core);
                            AddFeatureCollection(line.Name, mcu.Package);
                            AddFeatureCollection(line.Name, mcu.Name);

                            AddFeatureCollection(mcu.Core, company.Name);
                            AddFeatureCollection(mcu.Core, series.Name);
                            AddFeatureCollection(mcu.Core, line.Name);
                            AddFeatureCollection(mcu.Core, mcu.Package);
                            AddFeatureCollection(mcu.Core, mcu.Name);

                            AddFeatureCollection(mcu.Package, company.Name);
                            AddFeatureCollection(mcu.Package, series.Name);
                            AddFeatureCollection(mcu.Package, line.Name);
                            AddFeatureCollection(mcu.Package, mcu.Core);
                            AddFeatureCollection(mcu.Package, mcu.Name);

                            _mcuList.Add(mcu.Name);

                            if (!coreList.Contains(mcu.Core))
                                coreList.Add(mcu.Core);

                            if (!packageList.Contains(mcu.Package))
                                packageList.Add(mcu.Package);
                        }
                    }
                }
            }

            ComboBoxMCUName.ItemsSource = _mcuList;

            foreach (var item in coreList) {
                CheckListBoxCore.Items.Add(new CheckListBoxItem {
                    Content = item
                });
            }

            foreach (var item in packageList) {
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
                    if (SearchText.IsNullOrEmpty()) {
                        if (_featureFilter.Contains(data) ||
                            _featureCollection[data].Intersect(_featureFilter).Any() ||
                            _featureFilter.Count == 0) {
                            listBoxItem.IsEnabled = true;
                        }
                        else {
                            listBoxItem.IsSelected = false;
                            listBoxItem.IsEnabled = false;
                        }
                    }
                    else {
                        if (_featureCollection[data].Contains(SearchText)) {
                            listBoxItem.IsEnabled = true;
                        }
                        else {
                            listBoxItem.IsSelected = false;
                            listBoxItem.IsEnabled = false;
                        }
                    }
                }
            }
        }
    }
}