'use client';

import { Company, SERVICE_LABELS, ServiceTag } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface CompanyCardProps {
  company: Company;
}

export function CompanyCard({ company }: CompanyCardProps) {
  const primaryPhone = company.contacts?.find(
    (c) => c.is_primary && (c.type === 'phone_mobile' || c.type === 'phone_landline')
  ) || company.contacts?.find(
    (c) => c.type === 'phone_mobile' || c.type === 'phone_landline'
  );

  const primaryEmail = company.contacts?.find((c) => c.type === 'email');
  const headquarters = company.locations?.find((l) => l.type === 'headquarters') || company.locations?.[0];

  return (
    <Card className="hover:shadow-lg transition-shadow duration-200 h-full flex flex-col">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-lg font-semibold text-slate-900 leading-tight">
            {company.name}
          </CardTitle>
          <div className="flex gap-1 flex-shrink-0">
            {company.is_verified && (
              <Badge variant="default" className="bg-green-600 hover:bg-green-700 text-xs">
                ✅ DSP
              </Badge>
            )}
            {company.is_non_stop && (
              <Badge variant="secondary" className="text-xs">
                24/7
              </Badge>
            )}
          </div>
        </div>
        {company.motto && (
          <p className="text-sm text-slate-500 italic mt-1">
            "{company.motto}"
          </p>
        )}
      </CardHeader>

      <CardContent className="flex-1 flex flex-col">
        {/* Location with city/county */}
        {headquarters && (
          <div className="flex items-start gap-2 text-sm text-slate-600 mb-3">
            <span className="text-lg">📍</span>
            <div>
              <span>{headquarters.address}</span>
              {(headquarters.city || headquarters.county) && (
                <div className="text-xs text-slate-400 mt-0.5">
                  {headquarters.city}{headquarters.city && headquarters.county && ', '}{headquarters.county}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Phone */}
        {primaryPhone && (
          <div className="flex items-center gap-2 text-sm mb-3">
            <span className="text-lg">📞</span>
            <a
              href={`tel:${primaryPhone.value}`}
              className="text-blue-600 hover:underline font-medium"
            >
              {primaryPhone.value}
            </a>
          </div>
        )}

        {/* Services */}
        {company.services && company.services.length > 0 && (
          <div className="mt-auto pt-3 border-t">
            <div className="flex flex-wrap gap-1">
              {company.services.slice(0, 4).map((service) => {
                const label = SERVICE_LABELS[service.service_tag as ServiceTag];
                return (
                  <Badge
                    key={service.id}
                    variant="outline"
                    className="text-xs font-normal"
                  >
                    {label?.ro || service.service_tag}
                  </Badge>
                );
              })}
              {company.services.length > 4 && (
                <Badge variant="outline" className="text-xs font-normal">
                  +{company.services.length - 4}
                </Badge>
              )}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 mt-4">
          {primaryPhone && (
            <a
              href={`tel:${primaryPhone.value}`}
              className="flex-1 bg-blue-600 text-white text-center py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
            >
              📞 Sună acum
            </a>
          )}
          {company.website && (
            <a
              href={company.website}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 border border-slate-300 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors"
            >
              🌐
            </a>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
