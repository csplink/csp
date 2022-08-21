using Prism.Regions;
using System.Collections.Specialized;
using System.Windows;

namespace CSP.Apps.Dev.RegionAdapter.DockingManager
{
    public class RegionAdapter : RegionAdapterBase<Syncfusion.Windows.Tools.Controls.DockingManager>
    {
        public RegionAdapter(IRegionBehaviorFactory regionBehaviorFactory) : base(regionBehaviorFactory)
        {
        }

        protected override void Adapt(IRegion region, Syncfusion.Windows.Tools.Controls.DockingManager regionTarget)
        {
            region.Views.CollectionChanged += (_, e) =>
            {
                if (e.Action == NotifyCollectionChangedAction.Add)
                {
                    if (e.NewItems != null)
                    {
                        foreach (FrameworkElement element in e.NewItems)
                        {
                            if (!regionTarget.Children.Contains(element))
                            {
                                regionTarget.BeginInit();
                                regionTarget.Children.Add(element);
                                regionTarget.EndInit();
                            }
                        }
                    }
                }
            };
        }

        protected override void AttachBehaviors(IRegion region, Syncfusion.Windows.Tools.Controls.DockingManager regionTarget)
        {
            base.AttachBehaviors(region, regionTarget);
            if (!region.Behaviors.ContainsKey(DocumentRegionActiveAwareBehavior.BehaviorKey))
            {
                region.Behaviors.Add(DocumentRegionActiveAwareBehavior.BehaviorKey, new DocumentRegionActiveAwareBehavior { HostControl = regionTarget });
            }
        }

        protected override IRegion CreateRegion()
        {
            return new SingleActiveRegion();
        }
    }
}