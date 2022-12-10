using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.Windows;
using CSP.Models.DB.Chip;
using Syncfusion.Data;
using Syncfusion.UI.Xaml.Grid;

namespace CSP.Modules.Dialogs.NewMCU.Views.Components;

using repository_t =
    Dictionary<string, Dictionary<string, Dictionary<string, Dictionary<string, RepositoryModel.MCUModel>>>>;

public partial class MCUBox
{
    public static readonly DependencyProperty CompanyFilterProperty = DependencyProperty.Register("CompanyFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnCompanyFilterChanged)
            { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty CoreFilterProperty = DependencyProperty.Register("CoreFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnCoreFilterChanged)
            { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty LineFilterProperty = DependencyProperty.Register("LineFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnLineFilterChanged)
            { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty PackageFilterProperty = DependencyProperty.Register("PackageFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnPackageFilterChanged)
            { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty RepositoryProperty = DependencyProperty.Register("Repository",
        typeof(repository_t),
        typeof(MCUBox),
        new FrameworkPropertyMetadata(null, OnRepositoryChanged) { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty SearchTextProperty = DependencyProperty.Register("SearchText",
        typeof(string),
        typeof(MCUBox),
        new FrameworkPropertyMetadata("", OnSearchTextChanged) { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty SelectedMCUProperty = DependencyProperty.Register("SelectedMCU",
        typeof(RepositoryModel.MCUModel),
        typeof(MCUBox),
        new FrameworkPropertyMetadata(null, OnSelectedMCUChanged) { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty SeriesFilterProperty = DependencyProperty.Register("SeriesFilter",
        typeof(ObservableCollection<string>),
        typeof(MCUBox),
        new FrameworkPropertyMetadata(new ObservableCollection<string>(), OnSeriesFilterChanged)
            { BindsTwoWayByDefault = true });

    private readonly ObservableCollection<RepositoryModel.MCUModel> _mcuCollection = new();

    private ICollectionViewAdv _dataGridMCUView;

    public MCUBox() {
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

    public RepositoryModel.MCUModel SelectedMCU {
        get => (RepositoryModel.MCUModel)GetValue(SelectedMCUProperty);
        set => SetValue(SelectedMCUProperty, value);
    }


    public ObservableCollection<string> SeriesFilter {
        get => (ObservableCollection<string>)GetValue(SeriesFilterProperty);
        set => SetValue(SeriesFilterProperty, value);
    }

    private static void OnCompanyFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUBox)d).OnCompanyFilterValueChanged(e);
    }

    private static void OnCoreFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUBox)d).OnCoreFilterValueChanged(e);
    }

    private static void OnLineFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUBox)d).OnLineFilterValueChanged(e);
    }

    private static void OnPackageFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUBox)d).OnPackageFilterValueChanged(e);
    }

    private static void OnRepositoryChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUBox)d).OnRepositoryValueChanged(e);
    }

    private static void OnSearchTextChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUBox)d).OnSearchTextValueChanged(e);
    }

    private static void OnSelectedMCUChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUBox)d).OnSelectedMCUValueChanged(e);
    }

    private static void OnSeriesFilterChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((MCUBox)d).OnSeriesFilterValueChanged(e);
    }

    private void OnCompanyFilterValueChanged(DependencyPropertyChangedEventArgs e) {
        if (e.OldValue is ObservableCollection<string> oldValue) {
            oldValue.CollectionChanged -= OnFilterCollectionChanged;
        }

        if (e.NewValue is not ObservableCollection<string> newValue) {
            return;
        }

        newValue.CollectionChanged += OnFilterCollectionChanged;
    }

    private void OnCoreFilterValueChanged(DependencyPropertyChangedEventArgs e) {
        if (e.OldValue is ObservableCollection<string> oldValue) {
            oldValue.CollectionChanged -= OnFilterCollectionChanged;
        }

        if (e.NewValue is not ObservableCollection<string> newValue) {
            return;
        }

        newValue.CollectionChanged += OnFilterCollectionChanged;
    }

    private void OnDataGridMCUSelectionChanged(object sender, GridSelectionChangedEventArgs e) {
        if (sender is not SfDataGrid grid) {
            return;
        }

        if (grid.SelectedItem == null) {
            SelectedMCU = null;
        }
        else {
            SelectedMCU = (RepositoryModel.MCUModel)grid.SelectedItem;
        }
    }


    private bool OnDataGridMCUViewFilterRecords(object o) {
        if (o is not RepositoryModel.MCUModel item) {
            return false;
        }

        if (string.IsNullOrWhiteSpace(SearchText)
            && CompanyFilter.Count == 0
            && CoreFilter.Count == 0
            && SeriesFilter.Count == 0
            && LineFilter.Count == 0
            && PackageFilter.Count == 0
           ) {
            return true;
        }

        bool rtn = true;
        if (SearchText?.Length > 0) {
            string str = SearchText.ToUpper();
            rtn &= item.Name.ToUpper().Contains(str);
        }

        if (CompanyFilter.Count > 0) {
            rtn &= CompanyFilter.Contains(item.Company);
        }

        if (CoreFilter.Count > 0) {
            rtn &= CoreFilter.Contains(item.Core);
        }

        if (SeriesFilter.Count > 0) {
            rtn &= SeriesFilter.Contains(item.Series);
        }

        if (LineFilter.Count > 0) {
            rtn &= LineFilter.Contains(item.Line);
        }

        if (PackageFilter.Count > 0) {
            rtn &= PackageFilter.Contains(item.Package);
        }

        return rtn;
    }

    private void OnFilterCollectionChanged(object sender, NotifyCollectionChangedEventArgs e) {
        RefreshDataGridMCUViewFilter();
    }

    private void OnLineFilterValueChanged(DependencyPropertyChangedEventArgs e) {
        if (e.OldValue is ObservableCollection<string> oldValue) {
            oldValue.CollectionChanged -= OnFilterCollectionChanged;
        }

        if (e.NewValue is not ObservableCollection<string> newValue) {
            return;
        }

        newValue.CollectionChanged += OnFilterCollectionChanged;
    }

    private void OnPackageFilterValueChanged(DependencyPropertyChangedEventArgs e) {
        if (e.OldValue is ObservableCollection<string> oldValue) {
            oldValue.CollectionChanged -= OnFilterCollectionChanged;
        }

        if (e.NewValue is not ObservableCollection<string> newValue) {
            return;
        }

        newValue.CollectionChanged += OnFilterCollectionChanged;
    }

    private void OnRepositoryValueChanged(DependencyPropertyChangedEventArgs e) {
        if (e.NewValue is not repository_t repository) {
            return;
        }

        _mcuCollection.Clear();

        foreach (var (_, companies) in repository) {
            foreach (var (_, series) in companies) {
                foreach (var (_, lines) in series) {
                    foreach (var (_, mcu) in lines) {
                        _mcuCollection.Add(mcu);
                    }
                }
            }
        }

        DataGridMCU.ItemsSource = _mcuCollection;
    }

    private void OnSearchTextValueChanged(DependencyPropertyChangedEventArgs e) {
        RefreshDataGridMCUViewFilter();
    }

    private void OnSelectedMCUValueChanged(DependencyPropertyChangedEventArgs e) {
    }

    private void OnSeriesFilterValueChanged(DependencyPropertyChangedEventArgs e) {
        if (e.OldValue is ObservableCollection<string> oldValue) {
            oldValue.CollectionChanged -= OnFilterCollectionChanged;
        }

        if (e.NewValue is not ObservableCollection<string> newValue) {
            return;
        }

        newValue.CollectionChanged += OnFilterCollectionChanged;
    }

    private void RefreshDataGridMCUViewFilter() {
        if (_dataGridMCUView == null) {
            _dataGridMCUView = DataGridMCU.View;
            if (_dataGridMCUView != null) {
                _dataGridMCUView.Filter = OnDataGridMCUViewFilterRecords;
            }
        }

        _dataGridMCUView?.RefreshFilter();
    }
}