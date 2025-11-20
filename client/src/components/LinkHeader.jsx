import LinkIcon from './LinkIcon';

export default function LinkHeader({ link, linkIcon, title, siteName }) {
  return (
    <div className="flex flex-col">
      <a href={link} target="_blank">
        <div className="flex flex-row gap-2 items-center">
          <LinkIcon linkIcon={linkIcon} title={title} />
          <div className="grid grid-rows-2 h-full ">
            <span className="font-medium text-sm ">{siteName}</span>
            <span className="text-muted-foreground text-xs">{link}</span>
          </div>
        </div>
        <h3 className="text-lg font-medium hover:underline text-blue-800">
          {' '}
          {title}
        </h3>
      </a>{' '}
    </div>
  );
}
