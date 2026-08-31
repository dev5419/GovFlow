import { ReportViewer } from "@/modules/officer-report/components/ReportViewer";
import { DecisionLogTable } from "@/modules/officer-report/components/DecisionLogTable";
import { DownloadReportButton } from "@/modules/officer-report/components/DownloadReportButton";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function OfficerReportPage({ params }: { params: { tenderId: string; bidderId: string } }) {
  return (
    <main className="min-h-screen bg-slate-50 py-8 px-4 print:bg-white print:py-0 print:px-0">
      <div className="max-w-5xl mx-auto mb-6 flex items-center justify-between print:hidden">
        <Link 
          href={`/tenders/${params.tenderId}/dashboard`}
          className="flex items-center gap-2 text-sm text-[var(--color-primary)] font-medium hover:underline"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
        <DownloadReportButton tenderId={params.tenderId} bidderId={params.bidderId} />
      </div>

      <ReportViewer tenderId={params.tenderId} bidderId={params.bidderId} />
      
      <div className="page-break-before-always print:mt-12">
        <DecisionLogTable bidderId={params.bidderId} />
      </div>
    </main>
  );
}