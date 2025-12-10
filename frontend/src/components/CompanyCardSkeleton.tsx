import { Card, CardContent, CardHeader } from '@/components/ui/card';

// Custom skeleton with gentle shimmer animation
function SkeletonShimmer({ className }: { className?: string }) {
  return (
    <div 
      className={`skeleton-animated rounded-lg ${className || ''}`}
      style={{ backgroundColor: 'var(--warm-grey)' }}
    />
  );
}

export function CompanyCardSkeleton() {
  return (
    <Card className="h-full flex flex-col bg-white border-warm-grey rounded-2xl !shadow-none">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <SkeletonShimmer className="h-6 w-3/4" />
          <SkeletonShimmer className="h-5 w-12" />
        </div>
        <SkeletonShimmer className="h-4 w-full mt-2" />
      </CardHeader>
      <CardContent className="flex-1 flex flex-col">
        <SkeletonShimmer className="h-4 w-full mb-3" />
        <SkeletonShimmer className="h-4 w-32 mb-3" />
        <div className="mt-auto pt-3 border-t border-warm-grey">
          <div className="flex gap-1.5">
            <SkeletonShimmer className="h-5 w-16" />
            <SkeletonShimmer className="h-5 w-20" />
            <SkeletonShimmer className="h-5 w-14" />
          </div>
        </div>
        <div className="flex gap-2 mt-4">
          <SkeletonShimmer className="h-11 flex-1 rounded-xl" />
          <SkeletonShimmer className="h-11 w-20 rounded-xl" />
        </div>
      </CardContent>
    </Card>
  );
}
